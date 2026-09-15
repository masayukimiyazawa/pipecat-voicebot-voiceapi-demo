#!/usr/bin/env python3
"""
Generate PowerPoint slides for Pipecat Voice Bot architecture
Supports both Japanese and English presentations
"""

import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor

def add_title_slide(prs, title, subtitle=""):
    """Add a title slide"""
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(25, 118, 210)  # Deep blue
    
    # Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(2.0), Inches(9), Inches(1.5))
    title_frame = title_box.text_frame
    title_frame.word_wrap = True
    p = title_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(54)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER
    
    # Subtitle
    if subtitle:
        subtitle_box = slide.shapes.add_textbox(Inches(0.5), Inches(3.7), Inches(9), Inches(1.5))
        subtitle_frame = subtitle_box.text_frame
        subtitle_frame.word_wrap = True
        p = subtitle_frame.paragraphs[0]
        p.text = subtitle
        p.font.size = Pt(28)
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER
    
    return slide

def add_content_slide(prs, title, content_list):
    """Add a content slide with bullet points"""
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 245, 245)
    
    # Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    p = title_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = RGBColor(25, 118, 210)
    
    # Content
    content_box = slide.shapes.add_textbox(Inches(0.7), Inches(1.4), Inches(8.6), Inches(5.5))
    text_frame = content_box.text_frame
    text_frame.word_wrap = True
    
    for i, content in enumerate(content_list):
        if i == 0:
            p = text_frame.paragraphs[0]
        else:
            p = text_frame.add_paragraph()
        
        if isinstance(content, tuple):
            text, level = content
            p.level = level
        else:
            text = content
            p.level = 0
        
        p.text = text
        p.font.size = Pt(18 - p.level * 2)
        p.font.color.rgb = RGBColor(50, 50, 50)
        p.space_before = Pt(6)
        p.space_after = Pt(6)
    
    return slide

def add_two_column_slide(prs, title, left_title, left_content, right_title, right_content):
    """Add a two-column slide"""
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 245, 245)
    
    # Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    p = title_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = RGBColor(25, 118, 210)
    
    # Left column
    left_header = slide.shapes.add_textbox(Inches(0.5), Inches(1.4), Inches(4.3), Inches(0.5))
    p = left_header.text_frame.paragraphs[0]
    p.text = left_title
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = RGBColor(25, 118, 210)
    
    left_box = slide.shapes.add_textbox(Inches(0.5), Inches(2.0), Inches(4.3), Inches(4.5))
    left_frame = left_box.text_frame
    left_frame.word_wrap = True
    for i, content in enumerate(left_content):
        if i == 0:
            p = left_frame.paragraphs[0]
        else:
            p = left_frame.add_paragraph()
        p.text = content
        p.font.size = Pt(16)
        p.space_before = Pt(4)
        p.space_after = Pt(4)
    
    # Right column
    right_header = slide.shapes.add_textbox(Inches(5.2), Inches(1.4), Inches(4.3), Inches(0.5))
    p = right_header.text_frame.paragraphs[0]
    p.text = right_title
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = RGBColor(56, 142, 60)
    
    right_box = slide.shapes.add_textbox(Inches(5.2), Inches(2.0), Inches(4.3), Inches(4.5))
    right_frame = right_box.text_frame
    right_frame.word_wrap = True
    for i, content in enumerate(right_content):
        if i == 0:
            p = right_frame.paragraphs[0]
        else:
            p = right_frame.add_paragraph()
        p.text = content
        p.font.size = Pt(16)
        p.space_before = Pt(4)
        p.space_after = Pt(4)
    
    return slide

def create_japanese_presentation():
    """Create Japanese PowerPoint presentation"""
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)
    
    # Slide 1: Title
    add_title_slide(prs, 
        "Pipecat Voice Bot",
        "詳細アーキテクチャドキュメント")
    
    # Slide 2: プロジェクト概要
    add_content_slide(prs, "プロジェクト概要", [
        "🎯 目的: ローカルLLMと日本語TTSを使用したリアルタイム音声対話ボット",
        "🌐 入出力: ブラウザビデオセッション / 電話（PSTN/Vonage Voice API）",
        "🔧 主要技術:",
        ("Pipecat: パイプラインオーケストレーション", 1),
        ("Vonage API: 音声・ビデオゲートウェイ", 1),
        ("LM Studio: ローカルLLM実行環境", 1),
        ("Whisper MLX: 高速音声認識（日本語対応）", 1),
        ("pyopenjtalk: 日本語テキスト読み上げ", 1),
        "📊 特徴: プライバシー重視（全ローカル実行）、低遅延、マルチセッション対応"
    ])
    
    # Slide 3: システムアーキテクチャ
    add_content_slide(prs, "システムアーキテクチャ", [
        "4つの主要レイヤー:",
        ("クライアント層: ブラウザUI + OpenTok SDK", 1),
        ("クラウド層: Vonage Video/Voice API + Audio Connector", 1),
        ("サーバー層: FastAPI + WebSocket + セッション管理", 1),
        ("処理層: Pipecat Pipeline（STT→LLM→TTS）", 1),
        "",
        "データフロー:",
        ("クライアント → Vonage クラウド → サーバー", 1),
        ("サーバー → Pipecat Pipeline → LM Studio/pyopenjtalk", 1),
        ("処理結果 → Vonage クラウド → クライアント", 1)
    ])
    
    # Slide 4: server.py - FastAPI サーバー
    add_content_slide(prs, "server.py: FastAPI サーバー", [
        "責務: HTTP/WebSocket インターフェース、Vonage 統合",
        "",
        "主要エンドポイント:",
        ("GET/POST /voice/webhook: 電話着信受信 (NCCO返却)", 1),
        ("POST /demo/connect: ビデオセッション作成", 1),
        ("POST /connect: 一般接続 (Video API用)", 1),
        ("GET /: HTML 静的ファイル配信", 1),
        ("WebSocket /ws: 双方向音声ストリーミング", 1),
        "",
        "セッション管理: _active_connectors 辞書で複数接続を追跡"
    ])
    
    # Slide 5: bot.py - Pipecat パイプライン
    add_content_slide(prs, "bot.py: Pipecat パイプライン", [
        "責務: 音声処理、STT/LLM/TTS 統合、会話管理",
        "",
        "初期化 (preload_models):",
        ("OpenAILLMService (LM Studio)", 1),
        ("WhisperSTTServiceMLX (Whisper)", 1),
        ("PiperPlusTTSService (日本語TTS)", 1),
        ("SileroVADAnalyzer (音声検出)", 1),
        ("LocalSmartTurnAnalyzerV3 (会話ターン検出)", 1),
        "",
        "重要な修正: LLMAssistantAggregator の TextFrame を下流に転送する Monkey-Patch"
    ])
    
    # Slide 6: Pipecat パイプラインフロー
    add_content_slide(prs, "Pipecat パイプラインフロー", [
        "1. Transport Input → AudioFrameLogger (デバッグ)",
        "2. VADProcessor (SileroVAD) → 音声/無音検出",
        "3. WhisperSTTServiceMLX → 音声 → テキスト",
        "4. LLMUserAggregator → 発話を LLMContext に追加",
        "5. OpenAILLMService (LM Studio) → テキスト → テキスト",
        "6. LLMAssistantAggregator → 応答を LLMContext + TTS に送信",
        "7. PiperPlusTTSService → テキスト → 音声フレーム",
        "8. Transport Output → クライアントに送信"
    ])
    
    # Slide 7: tts_piper_plus.py
    add_content_slide(prs, "tts_piper_plus.py: 日本語 TTS", [
        "目的: pyopenjtalk（日本語HTS音声合成）を Pipecat インターフェースでラップ",
        "",
        "機能:",
        ("非同期実行: スレッドプールで TTS 処理をブロッキング回避", 1),
        ("音声正規化: float64 → int16 に変換・クリップ", 1),
        ("チャンク化: 4096B 単位で TTSAudioRawFrame を生成", 1),
        ("パラメータ: 速度=1.0、ピッチ=0.0（調整可能）", 1),
        "",
        "利点: モデルダウンロード不要、軽量、高速"
    ])
    
    # Slide 8: static/index.html - UI
    add_content_slide(prs, "static/index.html: ブラウザ UI", [
        "技術: Vonage OpenTok SDK (バニラ JavaScript)",
        "",
        "機能:",
        ("接続ボタン: POST /demo/connect → Vonage セッション作成", 1),
        ("ステータス表示: 接続状態をリアルタイム更新", 1),
        ("ログパネル: イベント・エラーをタイムスタンプ付きで記録", 1),
        ("音声ストリーム: ボットのマイク音声を購読 (audioOnly=true)", 1),
        "",
        "セッション流: OT.initSession() → token で接続 → subscribe()"
    ])
    
    # Slide 9: データフロー (ビデオセッション)
    add_content_slide(prs, "データフロー: ビデオセッション", [
        "1. ユーザー: 「接続」ボタンをクリック",
        "2. ブラウザ: POST /demo/connect を呼び出し",
        "3. サーバー: Vonage Session 作成 → Audio Connector 起動",
        "4. ブラウザ: OT.initSession() でセッションに参加",
        "5. Vonage: Audio Connector が WebSocket に接続",
        "6. ボット: 初期挨拶を送信 (テキスト → TTS → 音声)",
        "7. 双方向: ユーザー音声 ↔ Vonage ↔ Pipecat Pipeline ↔ 応答音声"
    ])
    
    # Slide 10: データフロー (電話)
    add_content_slide(prs, "データフロー: 電話 (PSTN)", [
        "1. ユーザー: Vonage 電話番号にコール",
        "2. Vonage: GET /voice/webhook に request 送信",
        "3. サーバー: NCCO を返却 (WebSocket endpoint を指定)",
        "4. Vonage: 通話を自動的に WebSocket /ws に接続",
        "5. ボット: Pipecat Pipeline 開始",
        "6. 双方向: 電話音声 ↔ Vonage ↔ Pipecat ↔ 応答音声",
        "",
        "利点: ブラウザ不要、従来の電話で利用可能"
    ])
    
    # Slide 11: 依存関係とローカルモデル
    add_content_slide(prs, "依存関係とローカルモデル", [
        "Python パッケージ:",
        ("pipecat-ai: パイプライン・STT/TTS/LLM 統合", 1),
        ("vonage: Vonage Video/Voice API", 1),
        ("uvicorn: ASGI サーバー", 1),
        ("fastapi: Web フレームワーク", 1),
        "",
        "ローカルモデル (LM Studio 必須):",
        ("LLM: Gemma/Llama 等 (ユーザー選択可能)", 1),
        ("STT: Whisper (LARGE_V3_TURBO_Q4 推奨)", 1),
        ("TTS: pyopenjtalk (HTS ベース)"  , 1)
    ])
    
    # Slide 12: 環境変数設定
    add_content_slide(prs, "環境変数設定 (.env)", [
        "LM Studio:",
        ("LM_STUDIO_BASE_URL=http://localhost:1234/v1", 1),
        ("LM_MODEL=gemma-4-26B-A4B-it-MLX-8bit", 1),
        ("STT_LANGUAGE=ja", 1),
        "",
        "Vonage:",
        ("VONAGE_APPLICATION_ID=<your-app-id>", 1),
        ("VONAGE_PRIVATE_KEY=<path-or-raw-key>", 1),
        ("VONAGE_AUDIO_RATE=16000", 1),
        ("WS_URI=wss://<tunnel-url>/ws (オプション)", 1)
    ])
    
    # Slide 13: 起動手順
    add_content_slide(prs, "起動手順", [
        "1. LM Studio を localhost:1234 で起動",
        ("モデルをロード (Gemma/Llama など)", 1),
        "",
        "2. リポジトリを .env ファイルで設定",
        "",
        "3. Cloudflare Tunnel で公開",
        ("cloudflared tunnel run pipecat", 1),
        "",
        "4. FastAPI サーバーを起動",
        ("python server.py", 1),
        "",
        "5. ブラウザで Tunnel URL にアクセス",
        "6. 「接続」ボタンをクリック → 音声対話開始"
    ])
    
    # Slide 14: パイプライン設定の詳細
    add_content_slide(prs, "パイプライン設定の詳細", [
        "VAD (Voice Activity Detection):",
        ("信頼度: 0.5", 1),
        ("音声開始: 0.2 秒", 1),
        ("無音判定: 0.2 秒", 1),
        ("アイドル: 1.0 秒", 1),
        "",
        "STT:",
        ("言語: 日本語 (ja)", 1),
        ("no_speech_prob: 0.3 (無音判定を調整)", 1),
        "",
        "LLM:",
        ("システムプロンプト: 日本語、簡潔、TTS対応", 1)
    ])
    
    # Slide 15: 重要な技術的工夫
    add_content_slide(prs, "重要な技術的工夫", [
        "1. 状態リセット (_reset_service):",
        ("接続ごとに LLM/STT/TTS の内部状態をクリア", 1),
        ("複数接続での相互干渉を防止", 1),
        "",
        "2. Monkey-Patch (LLMAssistantAggregator):",
        ("TextFrame を downstream に転送", 1),
        ("TTS が応答を受け取れるように修正", 1),
        "",
        "3. Audio Connector 管理:",
        ("新接続時に古い connector を全て停止", 1),
        ("メモリリークを防止", 1)
    ])
    
    # Slide 16: エラーハンドリング
    add_content_slide(prs, "エラーハンドリング", [
        "サーバー側:",
        ("WebSocket 切断 → finally で確実に cleanup", 1),
        ("モデル読み込み失敗 → ログして続行 (実行時エラー)", 1),
        ("Connector 停止失敗 → warning ログのみ", 1),
        "",
        "パイプライン側:",
        ("STT タイムアウト → _ttfb_timeout_task を cancel", 1),
        ("LLM エラー → exception ログ → セッション終了", 1),
        "",
        "ブラウザ側:",
        ("接続失敗 → UI に状態表示", 1),
        ("ストリーム受信失敗 → ログのみ (UI継続)"  , 1)
    ])
    
    # Slide 17: パフォーマンス・最適化
    add_content_slide(prs, "パフォーマンス・最適化", [
        "モデル事前読み込み:",
        ("サーバー起動時に preload_models() で全モデルをメモリ展開", 1),
        ("初回接続の遅延を排除", 1),
        "",
        "Whisper MLX:",
        ("LARGE_V3_TURBO_Q4: 高速、高精度（Gemini 推奨）", 1),
        "",
        "非同期処理:",
        ("asyncio で I/O ブロッキング回避", 1),
        ("並列処理で低遅延を実現", 1),
        "",
        "グリーティング戦略:",
        ("即時 + 遅延の2つで ネットワーク遅延対応", 1)
    ])
    
    # Slide 18: セキュリティ考慮事項
    add_content_slide(prs, "セキュリティ考慮事項", [
        "プライバシー:",
        ("全処理がローカルで実行 → データ外部送信なし", 1),
        ("LLM・STT・TTS は LM Studio で実行", 1),
        "",
        "認証・認可:",
        ("Vonage API は SDK で認証 (private key 管理)", 1),
        ("環境変数で秘密情報を管理 (.env)", 1),
        "",
        "通信:",
        ("Tunnel URL は HTTPS/WSS で暗号化", 1),
        ("WebSocket は binary protocol で効率的", 1)
    ])
    
    # Slide 19: トラブルシューティング
    add_content_slide(prs, "トラブルシューティング", [
        "接続できない:",
        ("LM Studio が起動しているか確認", 1),
        ("Tunnel URL が正しいか確認 (WS_URI)", 1),
        ("Vonage 認証情報が正しいか確認", 1),
        "",
        "音声が途切れる:",
        ("ネットワーク遅延を確認", 1),
        ("LLM レスポンス時間が長すぎないか確認", 1),
        ("Whisper の no_speech_prob を調整", 1),
        "",
        "応答がない:",
        ("LLM モデルが正しくロードされているか確認", 1),
        ("Monkey-Patch が適用されているか確認", 1)
    ])
    
    # Slide 20: まとめ
    add_content_slide(prs, "まとめ", [
        "✓ モジュラー設計で各コンポーネントが独立",
        "✓ ローカル実行でプライバシー重視",
        "✓ Vonage 統合で多様な入出力に対応",
        "✓ Pipecat で複雑な音声処理を簡潔に実装",
        "✓ 日本語最適化で自然な対話を実現",
        "✓ マルチセッション対応で複数ユーザーをサポート",
        "",
        "今後の拡張:",
        ("感情分析・言語別対応", 1),
        ("複数 LLM モデルのサポート", 1),
        ("会話ログ・分析機能", 1)
    ])
    
    return prs

def create_english_presentation():
    """Create English PowerPoint presentation"""
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)
    
    # Slide 1: Title
    add_title_slide(prs, 
        "Pipecat Voice Bot",
        "Detailed Architecture Documentation")
    
    # Slide 2: Project Overview
    add_content_slide(prs, "Project Overview", [
        "🎯 Goal: Real-time voice dialogue bot using local LLM and Japanese TTS",
        "🌐 Input/Output: Browser video session / Phone (PSTN/Vonage Voice API)",
        "🔧 Key Technologies:",
        ("Pipecat: Pipeline orchestration", 1),
        ("Vonage API: Audio/video gateway", 1),
        ("LM Studio: Local LLM runtime", 1),
        ("Whisper MLX: Fast speech recognition (Japanese-ready)", 1),
        ("pyopenjtalk: Japanese text-to-speech", 1),
        "📊 Features: Privacy-focused (all local), low-latency, multi-session"
    ])
    
    # Slide 3: System Architecture
    add_content_slide(prs, "System Architecture", [
        "Four main layers:",
        ("Client Layer: Browser UI + OpenTok SDK", 1),
        ("Cloud Layer: Vonage Video/Voice API + Audio Connector", 1),
        ("Server Layer: FastAPI + WebSocket + Session Management", 1),
        ("Processing Layer: Pipecat Pipeline (STT→LLM→TTS)", 1),
        "",
        "Data Flow:",
        ("Client → Vonage Cloud → Server", 1),
        ("Server → Pipecat Pipeline → LM Studio/pyopenjtalk", 1),
        ("Results → Vonage Cloud → Client", 1)
    ])
    
    # Slide 4: server.py - FastAPI Server
    add_content_slide(prs, "server.py: FastAPI Server", [
        "Responsibility: HTTP/WebSocket interface, Vonage integration",
        "",
        "Main Endpoints:",
        ("GET/POST /voice/webhook: Receive incoming calls (return NCCO)", 1),
        ("POST /demo/connect: Create video session", 1),
        ("POST /connect: General connection (Video API)", 1),
        ("GET /: Serve static HTML", 1),
        ("WebSocket /ws: Bidirectional audio streaming", 1),
        "",
        "Session Management: _active_connectors dict tracks multiple connections"
    ])
    
    # Slide 5: bot.py - Pipecat Pipeline
    add_content_slide(prs, "bot.py: Pipecat Pipeline", [
        "Responsibility: Audio processing, STT/LLM/TTS integration, conversation management",
        "",
        "Initialization (preload_models):",
        ("OpenAILLMService (LM Studio)", 1),
        ("WhisperSTTServiceMLX (Whisper)", 1),
        ("PiperPlusTTSService (Japanese TTS)", 1),
        ("SileroVADAnalyzer (Voice activity detection)", 1),
        ("LocalSmartTurnAnalyzerV3 (Conversation turn detection)", 1),
        "",
        "Critical Fix: Monkey-Patch LLMAssistantAggregator to forward TextFrame downstream"
    ])
    
    # Slide 6: Pipecat Pipeline Flow
    add_content_slide(prs, "Pipecat Pipeline Flow", [
        "1. Transport Input → AudioFrameLogger (debugging)",
        "2. VADProcessor (SileroVAD) → Detect speech/silence",
        "3. WhisperSTTServiceMLX → Audio → Text",
        "4. LLMUserAggregator → Add utterance to LLMContext",
        "5. OpenAILLMService (LM Studio) → Text → Text",
        "6. LLMAssistantAggregator → Send response to LLMContext + TTS",
        "7. PiperPlusTTSService → Text → Audio frames",
        "8. Transport Output → Send to client"
    ])
    
    # Slide 7: tts_piper_plus.py
    add_content_slide(prs, "tts_piper_plus.py: Japanese TTS", [
        "Purpose: Wrap pyopenjtalk (Japanese HTS synthesis) in Pipecat interface",
        "",
        "Features:",
        ("Async execution: Use thread pool to avoid blocking TTS", 1),
        ("Audio normalization: Convert float64 → int16 with clipping", 1),
        ("Chunking: Generate TTSAudioRawFrame in 4096B units", 1),
        ("Parameters: Speed=1.0, Pitch=0.0 (adjustable)", 1),
        "",
        "Advantages: No model download needed, lightweight, fast"
    ])
    
    # Slide 8: static/index.html - UI
    add_content_slide(prs, "static/index.html: Browser UI", [
        "Technology: Vonage OpenTok SDK (vanilla JavaScript)",
        "",
        "Features:",
        ("Connect Button: POST /demo/connect → Create Vonage session", 1),
        ("Status Display: Update connection state in real-time", 1),
        ("Log Panel: Record events/errors with timestamp", 1),
        ("Audio Stream: Subscribe to bot's microphone (audioOnly=true)", 1),
        "",
        "Session Flow: OT.initSession() → Connect with token → Subscribe()"
    ])
    
    # Slide 9: Data Flow - Video Session
    add_content_slide(prs, "Data Flow: Video Session", [
        "1. User clicks 'Connect' button",
        "2. Browser calls POST /demo/connect",
        "3. Server creates Vonage Session → Launches Audio Connector",
        "4. Browser calls OT.initSession() → Join with token",
        "5. Vonage Audio Connector connects to WebSocket",
        "6. Bot sends greeting (Text → TTS → Audio)",
        "7. Bidirectional: User speech ↔ Vonage ↔ Pipecat ↔ Response audio"
    ])
    
    # Slide 10: Data Flow - Phone (PSTN)
    add_content_slide(prs, "Data Flow: Phone (PSTN)", [
        "1. User calls Vonage phone number",
        "2. Vonage sends GET /voice/webhook request",
        "3. Server returns NCCO (specify WebSocket endpoint)",
        "4. Vonage automatically connects call to WebSocket /ws",
        "5. Bot starts Pipecat Pipeline",
        "6. Bidirectional: Phone audio ↔ Vonage ↔ Pipecat ↔ Response audio",
        "",
        "Advantage: No browser needed, works with regular phone"
    ])
    
    # Slide 11: Dependencies & Local Models
    add_content_slide(prs, "Dependencies & Local Models", [
        "Python Packages:",
        ("pipecat-ai: Pipeline, STT/TTS/LLM integration", 1),
        ("vonage: Vonage Video/Voice API", 1),
        ("uvicorn: ASGI server", 1),
        ("fastapi: Web framework", 1),
        "",
        "Local Models (LM Studio required):",
        ("LLM: Gemma/Llama etc (user-selectable)", 1),
        ("STT: Whisper (LARGE_V3_TURBO_Q4 recommended)", 1),
        ("TTS: pyopenjtalk (HTS-based)", 1)
    ])
    
    # Slide 12: Environment Variables (.env)
    add_content_slide(prs, "Environment Variables (.env)", [
        "LM Studio:",
        ("LM_STUDIO_BASE_URL=http://localhost:1234/v1", 1),
        ("LM_MODEL=gemma-4-26B-A4B-it-MLX-8bit", 1),
        ("STT_LANGUAGE=ja", 1),
        "",
        "Vonage:",
        ("VONAGE_APPLICATION_ID=<your-app-id>", 1),
        ("VONAGE_PRIVATE_KEY=<path-or-raw-key>", 1),
        ("VONAGE_AUDIO_RATE=16000", 1),
        ("WS_URI=wss://<tunnel-url>/ws (optional)", 1)
    ])
    
    # Slide 13: Startup Steps
    add_content_slide(prs, "Startup Steps", [
        "1. Start LM Studio on localhost:1234",
        ("Load a model (Gemma/Llama etc)", 1),
        "",
        "2. Configure repository with .env file",
        "",
        "3. Expose with Cloudflare Tunnel",
        ("cloudflared tunnel run pipecat", 1),
        "",
        "4. Start FastAPI server",
        ("python server.py", 1),
        "",
        "5. Open Tunnel URL in browser",
        "6. Click 'Connect' button → Voice conversation starts"
    ])
    
    # Slide 14: Pipeline Configuration Details
    add_content_slide(prs, "Pipeline Configuration Details", [
        "VAD (Voice Activity Detection):",
        ("Confidence: 0.5", 1),
        ("Speech Start: 0.2 sec", 1),
        ("Silence Detection: 0.2 sec", 1),
        ("Idle: 1.0 sec", 1),
        "",
        "STT:",
        ("Language: Japanese (ja)", 1),
        ("no_speech_prob: 0.3 (adjust silence threshold)", 1),
        "",
        "LLM:",
        ("System Prompt: Japanese, concise, TTS-compatible", 1)
    ])
    
    # Slide 15: Important Technical Approaches
    add_content_slide(prs, "Important Technical Approaches", [
        "1. State Reset (_reset_service):",
        ("Clear LLM/STT/TTS internal state per connection", 1),
        ("Prevent cross-connection interference", 1),
        "",
        "2. Monkey-Patch (LLMAssistantAggregator):",
        ("Forward TextFrame downstream", 1),
        ("Enable TTS to receive responses", 1),
        "",
        "3. Audio Connector Management:",
        ("Stop all old connectors on new connection", 1),
        ("Prevent memory leaks", 1)
    ])
    
    # Slide 16: Error Handling
    add_content_slide(prs, "Error Handling", [
        "Server Side:",
        ("WebSocket disconnect → cleanup in finally block", 1),
        ("Model load failure → log and continue (runtime error)", 1),
        ("Connector stop failure → warning log only", 1),
        "",
        "Pipeline Side:",
        ("STT timeout → cancel _ttfb_timeout_task", 1),
        ("LLM error → exception log → end session", 1),
        "",
        "Browser Side:",
        ("Connection failure → show status", 1),
        ("Stream receive failure → log only (continue UI)", 1)
    ])
    
    # Slide 17: Performance & Optimization
    add_content_slide(prs, "Performance & Optimization", [
        "Model Pre-loading:",
        ("preload_models() on startup loads all models to memory", 1),
        ("Eliminates first-connection delay", 1),
        "",
        "Whisper MLX:",
        ("LARGE_V3_TURBO_Q4: Fast, high-accuracy (recommended)", 1),
        "",
        "Async Processing:",
        ("asyncio avoids I/O blocking", 1),
        ("Parallel processing achieves low-latency", 1),
        "",
        "Greeting Strategy:",
        ("Immediate + Delayed to handle network latency", 1)
    ])
    
    # Slide 18: Security Considerations
    add_content_slide(prs, "Security Considerations", [
        "Privacy:",
        ("All processing runs locally → no data sent externally", 1),
        ("LLM/STT/TTS run in LM Studio", 1),
        "",
        "Authentication & Authorization:",
        ("Vonage API secured by SDK (private key management)", 1),
        ("Secrets managed in environment variables (.env)", 1),
        "",
        "Communication:",
        ("Tunnel URL encrypted with HTTPS/WSS", 1),
        ("WebSocket uses binary protocol for efficiency", 1)
    ])
    
    # Slide 19: Troubleshooting
    add_content_slide(prs, "Troubleshooting", [
        "Cannot Connect:",
        ("Verify LM Studio is running", 1),
        ("Check Tunnel URL is correct (WS_URI)", 1),
        ("Verify Vonage credentials are correct", 1),
        "",
        "Audio Cuts Out:",
        ("Check network latency", 1),
        ("Verify LLM response time isn't too long", 1),
        ("Adjust Whisper no_speech_prob", 1),
        "",
        "No Response:",
        ("Verify LLM model is loaded correctly", 1),
        ("Verify Monkey-Patch is applied", 1)
    ])
    
    # Slide 20: Summary
    add_content_slide(prs, "Summary", [
        "✓ Modular design with independent components",
        "✓ Local execution prioritizes privacy",
        "✓ Vonage integration enables diverse input/output",
        "✓ Pipecat simplifies complex audio processing",
        "✓ Japanese optimization enables natural dialogue",
        "✓ Multi-session support handles multiple users",
        "",
        "Future Enhancements:",
        ("Emotion analysis & multi-language support", 1),
        ("Multiple LLM model support", 1),
        ("Conversation logging & analytics", 1)
    ])
    
    return prs

if __name__ == "__main__":
    doc_dir = Path(__file__).parent
    
    print("Generating Japanese presentation...")
    prs_jp = create_japanese_presentation()
    jp_file = doc_dir / "architecture-JP.pptx"
    prs_jp.save(str(jp_file))
    print(f"✓ Saved: {jp_file}")
    
    print("\nGenerating English presentation...")
    prs_en = create_english_presentation()
    en_file = doc_dir / "architecture-EN.pptx"
    prs_en.save(str(en_file))
    print(f"✓ Saved: {en_file}")
    
    print("\n" + "="*60)
    print("PowerPoint presentations created successfully!")
    print("="*60)
