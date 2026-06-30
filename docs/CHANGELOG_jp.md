# 変更履歴

このプロジェクトの全ての重要な変更はこのファイルに記録されます。

## [Unreleased] - 2026-06-30

### 追加
- **Voice API (PSTN) サポート**: 既存の Video API に加え、Vonage Voice API（電話）経由での接続をサポートしました。
- **NCCO Webhook エンドポイント**: `server.py` に `/voice/webhook` を実装し、Vonage Voice の着信を WebSocket 経由でボットにブリッジします。
- **自動環境設定**: `start.sh` を更新し、Cloudflare Tunnel URL を自動検出して `.env` の `WS_URI` と `VONAGE_WEBHOOK_URL` を更新します。
- **挨拶ロジック改善**: `bot.py` を修正し、接続時に `TextFrame` による初期挨拶を送信することで、ユーザー入力がない場合の LLM の "No user query found" エラーを防止します。
- **ドキュメント**: 新しいアーキテクチャ、デモフロー、API エンドポイント情報を `README.md`（英語）と `README-JP.md`（日本語）に更新しました。

### 変更
- **アーキテクチャ**: システムはデュアルモード接続をサポートするようになりました:
  - **Video モード**: クライアント（ブラウザ）→ Video Session → Audio Connector → ボット
  - **Voice モード**: 電話 → Voice API → Webhook/NCCO → ボット
- **デプロイ**: `start.sh` を macOS との互換性と自動 Cloudflare Tunnel 管理のために最適化しました。
- **設定**: `VONAGE_WEBHOOK_URL` を `.env.example` に追加しました。

### 修正
- **Voice API 接続問題**: WebSocket 接続が NCCO ブリッジ経由で適切に確立されるようにし、電話が即座に切断される問題を修正しました。
- **LLM プロンプトエラー**: 初期の `LLMRunFrame` をテキストベースの挨拶に置き換えることで、"No user query found in messages" エラーを修正しました。
