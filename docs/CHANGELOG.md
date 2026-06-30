# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased] - 2026-06-30

### Added
- **Voice API (PSTN) Support**: Added support for connecting via Vonage Voice API (phone calls) in addition to the existing Video API.
- **NCCO Webhook Endpoint**: Implemented `/voice/webhook` in `server.py` to handle inbound Vonage Voice calls and bridge them to the bot via WebSocket.
- **Automatic Environment Configuration**: Updated `start.sh` to automatically detect the Cloudflare Tunnel URL and update `WS_URI` and `VONAGE_WEBHOOK_URL` in `.env`.
- **Improved Greeting Logic**: Modified `bot.py` to send an initial greeting via `TextFrame` upon connection, preventing "No user query found" errors in the LLM when no user input is present.
- **Documentation**: Updated `README.md` (English) and `README-JP.md` (Japanese) with new architecture, demo flows, and API endpoint information.

### Changed
- **Architecture**: The system now supports a dual-mode connectivity:
  - **Video Mode**: Client (Browser) → Video Session → Audio Connector → Bot.
  - **Voice Mode**: Phone Call → Voice API → Webhook/NCCO → Bot.
- **Deployment**: Optimized `start.sh` for better compatibility with macOS and automatic Cloudflare Tunnel management.
- **Configuration**: Added `VONAGE_WEBHOOK_URL` to `.env.example`.

### Fixed
- **Voice API Connection Issue**: Fixed the issue where phone calls were disconnected immediately by ensuring the WebSocket connection is properly established via the NCCO bridge.
- **LLM Prompt Error**: Fixed the "No user query found in messages" error by replacing the initial `LLMRunFrame` with a friendly text-based greeting.
