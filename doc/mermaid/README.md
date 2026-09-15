# Pipecat Voice Bot - アーキテクチャダイアグラム

このディレクトリには、Pipecat Voice Bot プロジェクトの詳細なアーキテクチャダイアグラムが含まれています。

## 📊 ダイアグラム一覧

### システムアーキテクチャ

#### 日本語版
- [system_architecture_jp.md](system_architecture_jp.md) - Mermaid ソース
- [system_architecture_jp.svg](system_architecture_jp.svg) - SVG 画像
- [system_architecture_jp.png](system_architecture_jp.png) - PNG 画像

#### English Version
- [system_architecture_en.md](system_architecture_en.md) - Mermaid Source
- [system_architecture_en.svg](system_architecture_en.svg) - SVG Image
- [system_architecture_en.png](system_architecture_en.png) - PNG Image

---

### データフロー

#### 日本語版
- [data_flow_jp.md](data_flow_jp.md) - Mermaid ソース
- [data_flow_jp.svg](data_flow_jp.svg) - SVG 画像
- [data_flow_jp.png](data_flow_jp.png) - PNG 画像

#### English Version
- [data_flow_en.md](data_flow_en.md) - Mermaid Source
- [data_flow_en.svg](data_flow_en.svg) - SVG Image
- [data_flow_en.png](data_flow_en.png) - PNG Image

---

### Pipecat パイプラインフロー

#### 日本語版
- [pipeline_jp.md](pipeline_jp.md) - Mermaid ソース
- [pipeline_jp.svg](pipeline_jp.svg) - SVG 画像
- [pipeline_jp.png](pipeline_jp.png) - PNG 画像

#### English Version
- [pipeline_en.md](pipeline_en.md) - Mermaid Source
- [pipeline_en.svg](pipeline_en.svg) - SVG Image
- [pipeline_en.png](pipeline_en.png) - PNG Image

---

## 使用方法

### オンラインで表示
1. [Mermaid Live Editor](https://mermaid.live/) にアクセス
2. `.md` ファイルの内容をコピー
3. コードペイストして表示

### ローカルで編集
```bash
# npm をインストール
brew install node

# mermaid-cli をインストール
npm install -g @mermaid-js/mermaid-cli

# ダイアグラムを画像に変換
mmdc -i system_architecture_jp.md -o system_architecture_jp.png
```

### PowerPoint に挿入
1. `../architecture-JP.pptx` または `../architecture-EN.pptx` を開く
2. スライドに `.png` または `.svg` 画像を挿入
3. 適切にサイズ調整

---

## ダイアグラムの説明

### システムアーキテクチャ
ブラウザ/電話からボットまでの全体構成を表示します。
- 🌐 クライアント層（ブラウザ/電話）
- ☁️ クラウド層（Vonage）
- 🖥️ サーバー層（FastAPI）
- 🔧 処理層（Pipecat Pipeline）
- 💾 ローカルモデル（LM Studio/pyopenjtalk）

### データフロー
ユーザーの音声入力から応答出力までの処理フローを表示します。
- 音声入力 → VAD（音声検出）
- STT（音声認識）→ LLM（テキスト生成）
- TTS（音声合成）→ 音声出力

### Pipecat パイプライン
各処理ステップと設定パラメータを詳細に表示します。
- 入力フレーム → ログ → VAD → STT → LLM → TTS → 出力
- LLMContext による会話履歴管理
- 各サービスの設定値（サンプリングレート、信頼度など）

---

## 技術詳細

各ダイアグラムはフローチャート形式（Mermaid `graph TB/LR`）で作成されています。

### 色分け
- 🔵 青：入出力
- 🟠 オレンジ：クラウドサービス
- 🟣 紫：サーバー
- 🟢 緑：処理パイプライン
- 🩷 ピンク：ローカルモデル

---

## 関連ドキュメント

- `../architecture-JP.pptx` - 日本語 PowerPoint 資料（20 スライド）
- `../architecture-EN.pptx` - English PowerPoint slides (20 slides)
- `../../README.md` - プロジェクト README
- `../../bot.py` - Pipecat ボット実装
- `../../server.py` - FastAPI サーバー実装

---

**生成日**: 2026-09-15
**プロジェクト**: Pipecat Voice Bot - Vonage Unified Video API デモ
