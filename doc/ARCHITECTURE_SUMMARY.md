# Pipecat Voice Bot - アーキテクチャドキュメント完全ガイド

**生成日**: 2026-09-15  
**プロジェクト**: Pipecat Voice Bot - Vonage Unified Video API デモ  
**言語対応**: 日本語 / English

---

## 📋 ドキュメント構成

このディレクトリには、Pipecat Voice Bot プロジェクトの詳細なアーキテクチャドキュメントが含まれています。

### 🎯 主要ファイル

| ファイル | 説明 | 用途 |
|---------|------|------|
| **architecture-JP.pptx** | 日本語 PowerPoint 資料 (20 スライド) | 日本語でのプレゼンテーション・講座 |
| **architecture-EN.pptx** | 英語 PowerPoint 資料 (20 slides) | English presentations & training |
| **mermaid/** | Mermaid ダイアグラムと画像 | 詳細なアーキテクチャ図、テクニカル資料 |

---

## 📊 PowerPoint スライド概要

### 日本語版 (architecture-JP.pptx)

**全20スライド** 詳細構成:

1. **タイトルスライド** - プロジェクト紹介
2. **プロジェクト概要** - 目的・技術・特徴
3. **システムアーキテクチャ** - 4層構成
4. **server.py** - FastAPI サーバー詳細
5. **bot.py** - Pipecat パイプライン詳細
6. **Pipecat パイプラインフロー** - 処理フロー
7. **tts_piper_plus.py** - 日本語 TTS 実装
8. **static/index.html** - ブラウザ UI
9. **データフロー: ビデオセッション** - 接続フロー
10. **データフロー: 電話 (PSTN)** - 通話フロー
11. **依存関係とローカルモデル** - パッケージ構成
12. **環境変数設定 (.env)** - 設定項目
13. **起動手順** - セットアップガイド
14. **パイプライン設定の詳細** - 各パラメータ
15. **重要な技術的工夫** - 実装工夫
16. **エラーハンドリング** - エラー対応
17. **パフォーマンス・最適化** - 最適化技法
18. **セキュリティ考慮事項** - セキュリティ対策
19. **トラブルシューティング** - 問題解決
20. **まとめ** - プロジェクトの全体像・今後の拡張

### 英語版 (architecture-EN.pptx)

**20 Slides** with identical structure to Japanese version but in English.

---

## 🔧 Mermaid ダイアグラム

### 📁 mermaid/ フォルダ内容

#### 1. システムアーキテクチャ（全体構成）
- **ファイル**:
  - `system_architecture_jp.md` (Mermaid source)
  - `system_architecture_jp.svg` (Vector image, scalable)
  - `system_architecture_jp.png` (Raster image, print-ready)
  - `system_architecture_en.md`, `.svg`, `.png` (English version)

**表示内容**:
```
ブラウザ/電話 ──→ Vonage Cloud ──→ FastAPI Server ──→ Pipecat Pipeline ──→ Local Models
     ↑                                                                            ↓
     └─────────────────── 双方向音声ストリーミング ────────────────────────┘
```

- 🌐 クライアント層（Browser/Phone）
- ☁️ クラウド層（Vonage Video/Voice API）
- 🖥️ サーバー層（FastAPI + WebSocket）
- 🔧 処理層（Pipecat Pipeline: STT→LLM→TTS）
- 💾 ローカルモデル（LM Studio, pyopenjtalk）

---

#### 2. データフロー（処理の流れ）
- **ファイル**:
  - `data_flow_jp.md` (Mermaid source)
  - `data_flow_jp.svg` / `data_flow_jp.png`
  - `data_flow_en.md`, `.svg`, `.png`

**表示内容**:
```
ユーザー音声 → ブラウザ → Vonage → WebSocket → VAD → STT (Whisper) → LLM (LM Studio)
                                                                           ↓
                                                                       応答テキスト
                                                                           ↓
                        スピーカー ← Vonage ← WebSocket ← TTS (pyopenjtalk) ← LLMContext
```

処理ステップ:
1. 音声入力 (InputAudioRawFrame)
2. VAD - 音声検出
3. STT - 音声認識 (Whisper)
4. LLMContext - 会話履歴管理
5. LLM - テキスト生成 (LM Studio)
6. TTS - 音声合成 (pyopenjtalk)
7. 音声出力 (TTSAudioRawFrame)

---

#### 3. Pipecat パイプラインフロー（詳細設定）
- **ファイル**:
  - `pipeline_jp.md` (Mermaid source)
  - `pipeline_jp.svg` / `pipeline_jp.png`
  - `pipeline_en.md`, `.svg`, `.png`

**表示内容**:
```
Transport Input
    ↓
AudioFrameLogger (デバッグ)
    ↓
VADProcessor (SileroVAD)
    ├─ confidence: 0.5
    ├─ start: 0.2s, stop: 0.2s
    └─ idle: 1.0s
    ↓
WhisperSTTServiceMLX
    ├─ Language: ja
    └─ Model: LARGE_V3_TURBO_Q4
    ↓
LLMUserAggregator → LLMContext
    ↓
OpenAILLMService (LM Studio)
    └─ Base URL: localhost:1234/v1
    ↓
LLMAssistantAggregator → LLMContext
    ↓
PiperPlusTTSService
    ├─ Speed: 1.0
    ├─ Pitch: 0.0
    └─ Chunk: 4096B
    ↓
Transport Output
```

各コンポーネントの役割と設定値を詳細に表示します。

---

## 🖼️ ダイアグラムの使用方法

### 1. オンラインで表示・編集

**Mermaid Live Editor** (https://mermaid.live/) を使用:
1. `.md` ファイルの内容をコピー
2. Mermaid Live Editor に貼り付け
3. リアルタイムで表示・編集可能

### 2. ローカルで画像を表示

PNG/SVG ファイルをプレビューアで開く:
- **PNG**: 高解像度、印刷対応
- **SVG**: ベクタ形式、スケーラブル

### 3. PowerPoint に挿入

1. PowerPoint ファイル (`.pptx`) を開く
2. スライドを選択
3. 「挿入」→「画像」で `.svg` または `.png` を追加
4. 適切にリサイズして配置

```
推奨: SVG を使用（スケーラブル）
```

### 4. ドキュメントに埋め込み

Markdown でダイアグラムを表示:
```markdown
```mermaid
[content from .md file]
```
```

---

## 📖 各ドキュメントの対象者

| ドキュメント | 対象者 | 用途 |
|-------------|-------|------|
| **architecture-JP.pptx** | 日本語話者 | プレゼン、勉強会、デモ |
| **architecture-EN.pptx** | English speakers | Presentations, training, demos |
| **system_architecture.png/svg** | 技術リード、エンジニア | システム全体の理解 |
| **data_flow.png/svg** | 開発者、QA | 処理フローの把握 |
| **pipeline.png/svg** | ML エンジニア、Data Engineer | パイプライン詳細の理解 |

---

## 🎨 色分け規約（Mermaid ダイアグラム）

| 色 | 対象 | 例 |
|----|------|-----|
| 🔵 青 | 入出力・通信 | Transport, WebSocket, Audio Input/Output |
| 🟠 オレンジ | クラウドサービス | Vonage API, Audio Connector |
| 🟣 紫 | サーバー・ネットワーク | FastAPI Server, Session Management |
| 🟢 緑 | 処理・パイプライン | STT, LLM, TTS, VAD |
| 🩷 ピンク | ローカルモデル | LM Studio, pyopenjtalk, Whisper |
| 🟡 黄 | データ・コンテキスト | LLMContext, TextFrame |

---

## 📐 ファイル仕様

### PowerPoint (.pptx)

- **スライドサイズ**: 10 × 7.5 インチ（標準）
- **形式**: Office Open XML
- **スライド数**: 20 スライド
- **フォント**: システムフォント（日本語対応）
- **配色**: 青（主色）、白（背景）、グレー（テキスト）

**表示方法**:
1. PowerPoint、Google Slides、LibreOffice で開く
2. スライドショーモードで表示（F5）
3. 必要に応じてPDF出力

### Mermaid ダイアグラム

#### Markdown (.md)
- **形式**: Mermaid ソースコード
- **用途**: オンライン編集・版管理用
- **エディタ**: テキストエディタ、GitHub、Mermaid Live Editor

#### SVG (.svg)
- **形式**: スケーラブルベクタグラフィックス
- **用途**: Web、ドキュメント、プレゼン
- **利点**: 無限にスケール可能、ファイルサイズ小
- **制限**: 複雑なグラデーション・効果は限定的

#### PNG (.png)
- **形式**: ラスタグラフィックス
- **用途**: 印刷、固定表示、汎用
- **利点**: 全ブラウザ・アプリで表示可能
- **制限**: スケール時に品質低下

---

## 🔍 ドキュメントの内容詳細

### architecture-JP.pptx の各セクション

#### 第1部: 全体像（スライド1-3）
- プロジェクト目的と特徴
- システムアーキテクチャの4層構成
- 基本的なデータフロー

#### 第2部: コンポーネント詳細（スライド4-8）
- **server.py**: FastAPI サーバー・Vonage 統合
- **bot.py**: Pipecat パイプライン・モデル管理
- **tts_piper_plus.py**: 日本語 TTS 実装
- **static/index.html**: ブラウザ UI
- パイプラインフロー（8ステップ）

#### 第3部: 運用・デプロイ（スライド9-14）
- データフロー（ビデオセッション / 電話）
- 環境変数設定
- 起動手順
- パイプライン設定パラメータ

#### 第4部: 技術詳細・最適化（スライド15-19）
- 技術的工夫（状態リセット、Monkey-Patch）
- エラーハンドリング戦略
- パフォーマンス最適化
- セキュリティ考慮事項
- トラブルシューティングガイド

#### 第5部: 総括（スライド20）
- プロジェクトのまとめ
- 今後の拡張可能性

---

## 🚀 クイックスタート

### 1. すぐに内容を確認したい
```
→ PowerPoint ファイルを開く (architecture-JP.pptx または architecture-EN.pptx)
→ スライドショーモードで全スライドを確認
```

### 2. 技術者向け詳細を確認したい
```
→ mermaid/ フォルダの PNG/SVG ファイルを確認
→ 各ダイアグラムでシステム・データフロー・パイプラインを理解
```

### 3. 開発時にリファレンスとして使いたい
```
→ GitHub で mermaid/.md ファイルを開く（自動レンダリング）
→ Mermaid Live Editor で編集・カスタマイズ
```

### 4. プレゼンテーションで使いたい
```
→ PowerPoint ファイルで実施
→ またはダイアグラムの PNG を別途スライドに挿入
```

---

## 📋 ファイルサイズ一覧

```
doc/
├─ architecture-JP.pptx          (約 3.5 MB)
├─ architecture-EN.pptx          (約 3.5 MB)
├─ mermaid/
│  ├─ README.md                  (約 4 KB)
│  ├─ system_architecture_jp.md   (約 2 KB) → .svg (40 KB) + .png (66 KB)
│  ├─ system_architecture_en.md   (約 2 KB) → .svg (41 KB) + .png (62 KB)
│  ├─ data_flow_jp.md            (約 1.3 KB) → .svg (27 KB) + .png (11 KB)
│  ├─ data_flow_en.md            (約 1.3 KB) → .svg (27 KB) + .png (9 KB)
│  ├─ pipeline_jp.md             (約 1.3 KB) → .svg (23 KB) + .png (82 KB)
│  └─ pipeline_en.md             (約 1.3 KB) → .svg (23 KB) + .png (81 KB)
└─ generate_*.py                 (スクリプト)
```

**合計**: 約 7 MB

---

## ✅ 生成チェックリスト

- ✅ Mermaid ダイアグラム 6 個（3 種類 × 2 言語）
  - ✅ system_architecture_jp.md/svg/png
  - ✅ system_architecture_en.md/svg/png
  - ✅ data_flow_jp.md/svg/png
  - ✅ data_flow_en.md/svg/png
  - ✅ pipeline_jp.md/svg/png
  - ✅ pipeline_en.md/svg/png

- ✅ PowerPoint プレゼンテーション 2 個
  - ✅ architecture-JP.pptx (20 スライド)
  - ✅ architecture-EN.pptx (20 slides)

- ✅ ドキュメント
  - ✅ mermaid/README.md (インデックス)
  - ✅ doc/ARCHITECTURE_SUMMARY.md (このファイル)

---

## 🔗 参考リンク

- **Mermaid 公式**: https://mermaid.live/
- **Mermaid-CLI**: https://github.com/mermaid-js/mermaid-cli
- **プロジェクト README**: `../../README.md`
- **ボット実装**: `../../bot.py`
- **サーバー実装**: `../../server.py`

---

## 📝 ライセンスと利用規約

これらのドキュメントはプロジェクトの一部です。

- **PowerPoint**: プレゼンテーション・教育用途での利用を推奨
- **Mermaid ダイアグラム**: Wiki・ドキュメント・ブログへの埋め込み可
- **コンテンツ**: プロジェクトのライセンスに準拠

---

**作成者**: Kiro AI  
**生成日**: 2026-09-15  
**バージョン**: 1.0  
**最終更新**: 2026-09-15

---

## 📞 サポート・質問

質問やサポートが必要な場合:
1. GitHub Issues でバグ報告
2. Discussions で質問
3. README のトラブルシューティングを確認

---

**Happy Documentation! 🎉**
