#!/usr/bin/env python3
"""
Generate comprehensive architecture documentation with Mermaid diagrams and PowerPoint slides
for Pipecat Voice Bot project in both Japanese and English.
"""

import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor

# Ensure doc directory exists
doc_dir = Path(__file__).parent
doc_dir.mkdir(exist_ok=True)

# =====================================================================
# MERMAID DIAGRAMS
# =====================================================================

MERMAID_DIAGRAMS = {
    "system_architecture_jp": """graph TB
    subgraph Browser["🌐 ブラウザ/電話"]
        UI["UI<br/>接続ボタン<br/>ログ表示"]
        OpenTok["OpenTok SDK<br/>音声ストリーム管理"]
    end
    
    subgraph Vonage["☁️ Vonage Cloud"]
        Session["Vonage Session<br/>セッション管理"]
        AudioConnector["Audio Connector<br/>WebSocket Bridge"]
    end
    
    subgraph Server["🖥️ FastAPI Server<br/>server.py"]
        REST["REST API<br/>/demo/connect<br/>/voice/webhook"]
        WebSocket["WebSocket /ws<br/>フレームシリアライザ"]
        SessionMgmt["セッション管理<br/>_active_connectors"]
    end
    
    subgraph Pipeline["🔧 Pipecat Pipeline<br/>bot.py"]
        Transport["Transport Input<br/>入力フレーム"]
        AudioLogger["AudioLogger<br/>デバッグ出力"]
        VAD["VAD Processor<br/>音声検出"]
        STT["STT Service<br/>Whisper MLX"]
        UserAgg["User Aggregator<br/>LLMContext"]
        LLM["LLM Service<br/>LM Studio"]
        AssAgg["Assistant Aggregator<br/>LLMContext"]
        TTS["TTS Service<br/>PiperPlus"]
        TransportOut["Transport Output<br/>出力フレーム"]
    end
    
    subgraph LocalModels["💾 Local Models"]
        LMStudio["LM Studio<br/>LLM + Whisper"]
        PyOpenJTalk["pyopenjtalk<br/>日本語TTS"]
    end
    
    Browser -->|音声入力/出力| Vonage
    Vonage -->|WebSocket<br/>音声フレーム| Server
    Server -->|API接続| Vonage
    Server -->|ボット制御| Pipeline
    
    Transport --> AudioLogger
    AudioLogger --> VAD
    VAD --> STT
    STT --> UserAgg
    UserAgg --> LLM
    LLM --> AssAgg
    AssAgg --> TTS
    TTS --> TransportOut
    TransportOut -->|WebSocket| Server
    
    LLM -->|OpenAI API| LMStudio
    STT -.->|音声転送| LMStudio
    TTS -->|テキスト| PyOpenJTalk
    PyOpenJTalk -->|音声| TTS
    
    style Browser fill:#e1f5ff,stroke:#01579b,color:#000
    style Vonage fill:#fff3e0,stroke:#e65100,color:#000
    style Server fill:#f3e5f5,stroke:#4a148c,color:#000
    style Pipeline fill:#e8f5e9,stroke:#1b5e20,color:#000
    style LocalModels fill:#fce4ec,stroke:#880e4f,color:#000""",

    "system_architecture_en": """graph TB
    subgraph Browser["🌐 Browser/Phone"]
        UI["UI<br/>Connect Button<br/>Log Display"]
        OpenTok["OpenTok SDK<br/>Audio Stream Management"]
    end
    
    subgraph Vonage["☁️ Vonage Cloud"]
        Session["Vonage Session<br/>Session Management"]
        AudioConnector["Audio Connector<br/>WebSocket Bridge"]
    end
    
    subgraph Server["🖥️ FastAPI Server<br/>server.py"]
        REST["REST API<br/>/demo/connect<br/>/voice/webhook"]
        WebSocket["WebSocket /ws<br/>Frame Serializer"]
        SessionMgmt["Session Management<br/>_active_connectors"]
    end
    
    subgraph Pipeline["🔧 Pipecat Pipeline<br/>bot.py"]
        Transport["Transport Input<br/>Input Frames"]
        AudioLogger["AudioLogger<br/>Debug Output"]
        VAD["VAD Processor<br/>Speech Detection"]
        STT["STT Service<br/>Whisper MLX"]
        UserAgg["User Aggregator<br/>LLMContext"]
        LLM["LLM Service<br/>LM Studio"]
        AssAgg["Assistant Aggregator<br/>LLMContext"]
        TTS["TTS Service<br/>PiperPlus"]
        TransportOut["Transport Output<br/>Output Frames"]
    end
    
    subgraph LocalModels["💾 Local Models"]
        LMStudio["LM Studio<br/>LLM + Whisper"]
        PyOpenJTalk["pyopenjtalk<br/>Japanese TTS"]
    end
    
    Browser -->|Audio In/Out| Vonage
    Vonage -->|WebSocket<br/>Audio Frames| Server
    Server -->|API Connection| Vonage
    Server -->|Bot Control| Pipeline
    
    Transport --> AudioLogger
    AudioLogger --> VAD
    VAD --> STT
    STT --> UserAgg
    UserAgg --> LLM
    LLM --> AssAgg
    AssAgg --> TTS
    TTS --> TransportOut
    TransportOut -->|WebSocket| Server
    
    LLM -->|OpenAI API| LMStudio
    STT -.->|Audio Transfer| LMStudio
    TTS -->|Text| PyOpenJTalk
    PyOpenJTalk -->|Audio| TTS
    
    style Browser fill:#e1f5ff,stroke:#01579b,color:#000
    style Vonage fill:#fff3e0,stroke:#e65100,color:#000
    style Server fill:#f3e5f5,stroke:#4a148c,color:#000
    style Pipeline fill:#e8f5e9,stroke:#1b5e20,color:#000
    style LocalModels fill:#fce4ec,stroke:#880e4f,color:#000""",

    "data_flow_jp": """graph LR
    User["🎤 ユーザー<br/>発話"]
    
    Browser["ブラウザ<br/>マイク入力"]
    
    Vonage_In["Vonage<br/>音声受信"]
    
    WS_In["WebSocket<br/>入力"]
    
    VAD_Proc["VAD<br/>音声検出"]
    
    STT_Proc["Whisper STT<br/>音声→テキスト"]
    
    LLMContext["LLMContext<br/>会話履歴管理"]
    
    LLM_Proc["LM Studio LLM<br/>テキスト生成"]
    
    TTS_Proc["PiperPlus TTS<br/>テキスト→音声"]
    
    WS_Out["WebSocket<br/>出力"]
    
    Vonage_Out["Vonage<br/>音声送信"]
    
    Speaker["🔊 スピーカー<br/>応答を再生"]
    
    User -->|音声| Browser
    Browser -->|音声フレーム| Vonage_In
    Vonage_In -->|WebSocket| WS_In
    WS_In -->|InputAudioRawFrame| VAD_Proc
    VAD_Proc -->|音声検出| STT_Proc
    STT_Proc -->|TextFrame| LLMContext
    LLMContext -->|ユーザー入力| LLM_Proc
    LLM_Proc -->|TextFrame| LLMContext
    LLMContext -->|応答テキスト| TTS_Proc
    TTS_Proc -->|TTSAudioRawFrame| WS_Out
    WS_Out -->|WebSocket| Vonage_Out
    Vonage_Out -->|音声| Speaker
    
    style User fill:#ffebee,stroke:#c62828
    style Speaker fill:#c8e6c9,stroke:#2e7d32
    style STT_Proc fill:#bbdefb,stroke:#1565c0
    style LLM_Proc fill:#fff9c4,stroke:#f57f17
    style TTS_Proc fill:#f8bbd0,stroke:#c2185b""",

    "data_flow_en": """graph LR
    User["🎤 User<br/>Speech"]
    
    Browser["Browser<br/>Mic Input"]
    
    Vonage_In["Vonage<br/>Audio Reception"]
    
    WS_In["WebSocket<br/>Input"]
    
    VAD_Proc["VAD<br/>Speech Detection"]
    
    STT_Proc["Whisper STT<br/>Audio→Text"]
    
    LLMContext["LLMContext<br/>Conversation History"]
    
    LLM_Proc["LM Studio LLM<br/>Text Generation"]
    
    TTS_Proc["PiperPlus TTS<br/>Text→Audio"]
    
    WS_Out["WebSocket<br/>Output"]
    
    Vonage_Out["Vonage<br/>Audio Transmission"]
    
    Speaker["🔊 Speaker<br/>Playback Response"]
    
    User -->|Speech| Browser
    Browser -->|Audio Frames| Vonage_In
    Vonage_In -->|WebSocket| WS_In
    WS_In -->|InputAudioRawFrame| VAD_Proc
    VAD_Proc -->|Speech Detected| STT_Proc
    STT_Proc -->|TextFrame| LLMContext
    LLMContext -->|User Input| LLM_Proc
    LLM_Proc -->|TextFrame| LLMContext
    LLMContext -->|Response Text| TTS_Proc
    TTS_Proc -->|TTSAudioRawFrame| WS_Out
    WS_Out -->|WebSocket| Vonage_Out
    Vonage_Out -->|Audio| Speaker
    
    style User fill:#ffebee,stroke:#c62828
    style Speaker fill:#c8e6c9,stroke:#2e7d32
    style STT_Proc fill:#bbdefb,stroke:#1565c0
    style LLM_Proc fill:#fff9c4,stroke:#f57f17
    style TTS_Proc fill:#f8bbd0,stroke:#c2185b""",

    "pipeline_jp": """graph TB
    Input["Transport Input<br/>WebSocket入力"]
    
    Log["AudioFrameLogger<br/>デバッグログ"]
    
    VAD["VADProcessor<br/>SileroVAD<br/>confidence=0.5<br/>start=0.2s stop=0.2s"]
    
    STT["WhisperSTTServiceMLX<br/>言語: ja<br/>モデル: LARGE_V3_TURBO_Q4"]
    
    UserAgg["LLMUserAggregator<br/>会話履歴に追加<br/>timeout=5.0s"]
    
    LLM["OpenAILLMService<br/>ベースURL: localhost:1234/v1<br/>システムプロンプト: 日本語対応"]
    
    AssAgg["LLMAssistantAggregator<br/>Monkey-patch適用<br/>TextFrameを下流に転送"]
    
    TTS["PiperPlusTTSService<br/>pyopenjtalk<br/>速度: 1.0 ピッチ: 0.0<br/>チャンク: 4096B"]
    
    Output["Transport Output<br/>WebSocket出力"]
    
    Context["LLMContext<br/>会話メッセージ管理"]
    
    Input --> Log
    Log --> VAD
    VAD --> STT
    STT --> UserAgg
    UserAgg --> Context
    Context --> LLM
    LLM --> AssAgg
    AssAgg --> Context
    Context --> TTS
    TTS --> Output
    
    style Input fill:#e3f2fd,stroke:#1565c0
    style Output fill:#c8e6c9,stroke:#2e7d32
    style Context fill:#fff9c4,stroke:#f57f17
    style VAD fill:#bbdefb,stroke:#1565c0
    style STT fill:#c5cae9,stroke:#283593
    style LLM fill:#fff3e0,stroke:#e65100
    style TTS fill:#f8bbd0,stroke:#c2185b""",

    "pipeline_en": """graph TB
    Input["Transport Input<br/>WebSocket Input"]
    
    Log["AudioFrameLogger<br/>Debug Logging"]
    
    VAD["VADProcessor<br/>SileroVAD<br/>confidence=0.5<br/>start=0.2s stop=0.2s"]
    
    STT["WhisperSTTServiceMLX<br/>Language: ja<br/>Model: LARGE_V3_TURBO_Q4"]
    
    UserAgg["LLMUserAggregator<br/>Add to Conversation<br/>timeout=5.0s"]
    
    LLM["OpenAILLMService<br/>Base URL: localhost:1234/v1<br/>System Prompt: Japanese"]
    
    AssAgg["LLMAssistantAggregator<br/>Monkey-patch Applied<br/>Forward TextFrame Downstream"]
    
    TTS["PiperPlusTTSService<br/>pyopenjtalk<br/>Speed: 1.0 Pitch: 0.0<br/>Chunk: 4096B"]
    
    Output["Transport Output<br/>WebSocket Output"]
    
    Context["LLMContext<br/>Message Management"]
    
    Input --> Log
    Log --> VAD
    VAD --> STT
    STT --> UserAgg
    UserAgg --> Context
    Context --> LLM
    LLM --> AssAgg
    AssAgg --> Context
    Context --> TTS
    TTS --> Output
    
    style Input fill:#e3f2fd,stroke:#1565c0
    style Output fill:#c8e6c9,stroke:#2e7d32
    style Context fill:#fff9c4,stroke:#f57f17
    style VAD fill:#bbdefb,stroke:#1565c0
    style STT fill:#c5cae9,stroke:#283593
    style LLM fill:#fff3e0,stroke:#e65100
    style TTS fill:#f8bbd0,stroke:#c2185b"""
}

# Save Mermaid diagrams
mermaid_dir = doc_dir / "mermaid"
mermaid_dir.mkdir(exist_ok=True)

for name, diagram in MERMAID_DIAGRAMS.items():
    mermaid_file = mermaid_dir / f"{name}.md"
    mermaid_file.write_text(f"```mermaid\n{diagram}\n```\n")
    print(f"✓ Created: {mermaid_file}")

print("\n" + "="*60)
print("Mermaid diagrams created successfully!")
print("="*60)
