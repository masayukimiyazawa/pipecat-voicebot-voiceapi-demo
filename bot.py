import asyncio
import os

import numpy as np
from dotenv import load_dotenv
from loguru import logger

from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.audio.vad.vad_analyzer import VADParams
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.worker import PipelineParams, PipelineWorker
from pipecat.frames.frames import Frame, InputAudioRawFrame, TextFrame
from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.frame_processor import FrameDirection, FrameProcessor
from pipecat.processors.aggregators.llm_response_universal import (
    LLMAssistantAggregator,
    LLMContextAggregatorPair,
    LLMUserAggregatorParams,
)
from pipecat.runner.types import WebSocketRunnerArguments
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.services.whisper.stt import WhisperSTTServiceMLX, MLXModel
from pipecat.transcriptions.language import Language
from pipecat.services.settings import assert_given
from tts_piper_plus import PiperPlusTTSService
from pipecat.serializers.vonage import VonageFrameSerializer
from pipecat.transports.base_transport import BaseTransport
from pipecat.transports.websocket.fastapi import (
    FastAPIWebsocketParams,
    FastAPIWebsocketTransport,
)
from pipecat.workers.runner import WorkerRunner

load_dotenv(override=True)

class AudioFrameLogger(FrameProcessor):
    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)
        if isinstance(frame, InputAudioRawFrame):
            logger.debug(f"AudioFrameLogger: received {len(frame.audio)} bytes @ {frame.sample_rate}Hz")
        await self.push_frame(frame, direction)

# Monkey-patch LLMAssistantAggregator to forward TextFrames downstream to TTS.
# Pipecat 1.4.0's _handle_text absorbs text for context but does not push
# it to the next processor, starving the TTS service.
_original_handle_text = LLMAssistantAggregator._handle_text
async def _forwarding_handle_text(self, frame: TextFrame):
    await _original_handle_text(self, frame)
    await self.push_frame(frame, FrameDirection.DOWNSTREAM)
LLMAssistantAggregator._handle_text = _forwarding_handle_text

AUDIO_OUT_SAMPLE_RATE: int = 16_000

LM_STUDIO_BASE_URL = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
LM_MODEL = os.getenv("LM_MODEL", "")
STT_LANGUAGE = os.getenv("STT_LANGUAGE", "ja")

_llm_instance = None
_stt_instance = None
_tts_instance = None


async def preload_models():
    global _llm_instance, _stt_instance, _tts_instance
    
    logger.info("Pre-loading models (this may take a minute)...")
    
    _llm_instance = OpenAILLMService(
        base_url=LM_STUDIO_BASE_URL,
        api_key="not-needed",
        settings=OpenAILLMService.Settings(
            model=LM_MODEL,
            system_instruction=(
                "あなたは音声アシスタントです。"
                "応答はテキスト読み上げで読まれるため、簡潔で会話調にしてください。"
                "日本語と英語の両方に対応できます。"
                "記号やマークダウンは避けてください。"
            ),
        ),
    )

    _stt_instance = WhisperSTTServiceMLX(
        settings=WhisperSTTServiceMLX.Settings(
            model=MLXModel.LARGE_V3_TURBO_Q4,
            language=Language(STT_LANGUAGE),
            no_speech_prob=0.3,
        ),
    )

    _tts_instance = PiperPlusTTSService()

    # Force VAD model loading
    logger.info("Loading VAD model...")
    vad = SileroVADAnalyzer(
        params=VADParams(
            confidence=0.5,
            start_secs=0.2,
            stop_secs=0.2,
            min_volume=0.0,
        ),
    )
    del vad
    
    # Force Smart Turn model loading
    logger.info("Loading turn detection model...")
    from pipecat.audio.turn.smart_turn.local_smart_turn_v3 import LocalSmartTurnAnalyzerV3
    turn = LocalSmartTurnAnalyzerV3()
    del turn
    
    # Force Whisper model loading by triggering import and first transcribe
    logger.info("Loading Whisper STT model...")
    
    # Force mlx_whisper import and model loading with dummy audio
    dummy_audio = bytes(32000)  # 1 second of silence at 16kHz
    try:
        import mlx_whisper
        model_path = assert_given(_stt_instance._settings.model) if _stt_instance else None
        if model_path:
            # Transcribe dummy audio to force model loading
            audio_float = np.frombuffer(dummy_audio, dtype=np.int16).astype(np.float32) / 32768.0
            mlx_whisper.transcribe(
                audio_float,
                path_or_hf_repo=model_path,
                language="ja",
            )
            logger.info("Whisper model loaded successfully")
    except Exception as e:
        logger.debug(f"Model loading (may fail if model path not set): {e}")
    
    # Give time for models to load
    await asyncio.sleep(5)
    
    logger.info("All models pre-loaded successfully")


def get_llm():
    if _llm_instance is None:
        raise RuntimeError("Models not pre-loaded. Call preload_models() first.")
    return _llm_instance


def get_stt():
    if _stt_instance is None:
        raise RuntimeError("Models not pre-loaded. Call preload_models() first.")
    return _stt_instance


def get_tts():
    if _tts_instance is None:
        raise RuntimeError("Models not pre-loaded. Call preload_models() first.")
    return _tts_instance


async def run_bot(transport: BaseTransport, handle_sigint: bool, sample_rate: int):
    llm = get_llm()
    stt = get_stt()
    tts = get_tts()

    context = LLMContext()
    user_aggregator, assistant_aggregator = LLMContextAggregatorPair(
        context,
        user_params=LLMUserAggregatorParams(
            vad_analyzer=SileroVADAnalyzer(
                params=VADParams(
                    confidence=0.5,
                    start_secs=0.2,
                    stop_secs=0.2,
                    min_volume=0.0,
                ),
            ),
            audio_idle_timeout=1.0,
            user_turn_stop_timeout=5.0,
        ),
    )

    audio_logger = AudioFrameLogger()

    pipeline = Pipeline(
        [
            transport.input(),
            audio_logger,
            stt,
            user_aggregator,
            llm,
            assistant_aggregator,
            tts,
            transport.output(),
        ]
    )

    worker = PipelineWorker(
        pipeline,
        params=PipelineParams(
            audio_in_sample_rate=sample_rate,
            audio_out_sample_rate=AUDIO_OUT_SAMPLE_RATE,
            enable_metrics=True,
            enable_usage_metrics=True,
        ),
    )

    @transport.event_handler("on_client_connected")
    async def on_client_connected(_transport, _client):
        logger.info("Client connected. Waiting for user input...")

    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(_transport, _client):
        logger.info("Client disconnected. Ending session.")
        await worker.cancel()

    runner = WorkerRunner(handle_sigint=handle_sigint)
    await runner.add_workers(worker)
    await runner.run()


async def bot(runner_args: WebSocketRunnerArguments):
    # Default to 16000 if not specified, but allow override from environment
    sample_rate = int(os.getenv("VONAGE_AUDIO_RATE", "16000"))
    
    logger.info(f"Starting bot with sample rate: {sample_rate}")

    serializer = VonageFrameSerializer(
        VonageFrameSerializer.InputParams(
            vonage_sample_rate=sample_rate,
        )
    )

    transport = FastAPIWebsocketTransport(
        websocket=runner_args.websocket,
        params=FastAPIWebsocketParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
            audio_out_10ms_chunks=2,
            serializer=serializer,
        ),
    )

    await run_bot(transport, runner_args.handle_sigint, sample_rate)

