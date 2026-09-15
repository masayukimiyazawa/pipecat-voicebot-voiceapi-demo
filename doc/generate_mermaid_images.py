#!/usr/bin/env python3
"""
Generate Mermaid diagram images from markdown files using mermaid-cli
or fallback to creating SVG/PNG via browser automation if needed.
"""

import os
import subprocess
import json
from pathlib import Path

def check_mermaid_cli():
    """Check if mermaid-cli is installed"""
    try:
        result = subprocess.run(['mmdc', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_mermaid_cli():
    """Install mermaid-cli via npm"""
    print("Installing mermaid-cli...")
    try:
        subprocess.run(['npm', 'install', '-g', '@mermaid-js/mermaid-cli'], check=True)
        return True
    except subprocess.CalledProcessError:
        print("⚠️  Failed to install mermaid-cli. Trying alternative method...")
        return False

def generate_mermaid_images_with_cli(mermaid_cli_available):
    """Generate images using mermaid-cli"""
    doc_dir = Path(__file__).parent
    mermaid_dir = doc_dir / "mermaid"
    
    if not mermaid_cli_available and not install_mermaid_cli():
        return False
    
    md_files = list(mermaid_dir.glob("*.md"))
    
    for md_file in md_files:
        base_name = md_file.stem
        svg_file = mermaid_dir / f"{base_name}.svg"
        png_file = mermaid_dir / f"{base_name}.png"
        
        try:
            # Generate SVG
            cmd = ['mmdc', '-i', str(md_file), '-o', str(svg_file), '-t', 'default']
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✓ Generated SVG: {svg_file}")
            
            # Generate PNG
            cmd = ['mmdc', '-i', str(md_file), '-o', str(png_file), '-t', 'default']
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✓ Generated PNG: {png_file}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Failed to generate images for {base_name}: {e}")
    
    return True

def generate_mermaid_images_with_browser():
    """Generate images using browser automation as fallback"""
    print("\n⚠️  Using browser-based image generation...")
    print("This requires a web browser. Installing required packages...")
    
    try:
        subprocess.run(['pip', 'install', '-q', 'playwright'], check=True)
        subprocess.run(['playwright', 'install', 'chromium'], check=True)
    except subprocess.CalledProcessError:
        print("⚠️  Could not install Playwright. Skipping image generation.")
        return False
    
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("⚠️  Playwright not available. Skipping image generation.")
        return False
    
    doc_dir = Path(__file__).parent
    mermaid_dir = doc_dir / "mermaid"
    md_files = list(mermaid_dir.glob("*.md"))
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        for md_file in md_files:
            try:
                base_name = md_file.stem
                
                # Read mermaid diagram
                with open(md_file, 'r') as f:
                    content = f.read()
                    # Extract mermaid code from markdown
                    mermaid_code = content.split('```mermaid\n')[1].split('\n```')[0]
                
                # Create HTML with mermaid
                html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {{ margin: 0; padding: 20px; background: #f5f5f5; }}
        .mermaid {{ background: white; padding: 20px; display: inline-block; }}
    </style>
</head>
<body>
    <div class="mermaid">
{mermaid_code}
    </div>
    <script>
        mermaid.contentLoaded();
    </script>
</body>
</html>
"""
                
                # Create temporary HTML file
                temp_html = mermaid_dir / f"temp_{base_name}.html"
                temp_html.write_text(html_content)
                
                # Render to PNG
                page = browser.new_page()
                page.goto(f"file://{temp_html.absolute()}")
                page.wait_for_load_state('networkidle')
                
                png_file = mermaid_dir / f"{base_name}.png"
                page.screenshot(path=str(png_file), full_page=True)
                print(f"✓ Generated PNG: {png_file}")
                
                # Clean up
                temp_html.unlink()
                page.close()
            
            except Exception as e:
                print(f"⚠️  Error generating image for {md_file.name}: {e}")
        
        browser.close()
    
    return True

def create_markdown_index():
    """Create an index markdown file linking all diagrams"""
    doc_dir = Path(__file__).parent
    mermaid_dir = doc_dir / "mermaid"
    
    index_content = """# Pipecat Voice Bot - アーキテクチャダイアグラム

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
"""
    
    index_file = mermaid_dir / "README.md"
    index_file.write_text(index_content)
    print(f"✓ Created index: {index_file}")

def main():
    doc_dir = Path(__file__).parent
    mermaid_dir = doc_dir / "mermaid"
    
    print("="*60)
    print("Mermaid Image Generation")
    print("="*60)
    
    # Try mermaid-cli first
    mermaid_cli_available = check_mermaid_cli()
    
    if mermaid_cli_available:
        print("\n✓ mermaid-cli is available")
        success = generate_mermaid_images_with_cli(mermaid_cli_available)
    else:
        print("\n⚠️  mermaid-cli not found")
        success = generate_mermaid_images_with_browser()
    
    # Create index markdown
    print("\nCreating index markdown...")
    create_markdown_index()
    
    if success:
        print("\n" + "="*60)
        print("✓ Image generation completed!")
        print("="*60)
        print("\nGenerated files in ./mermaid/:")
        for file in sorted(mermaid_dir.glob("*")):
            if file.is_file():
                print(f"  - {file.name}")
    else:
        print("\n" + "="*60)
        print("⚠️  Image generation partially completed")
        print("="*60)
        print("\nMermaid source files are available:")
        for file in sorted(mermaid_dir.glob("*.md")):
            if file.is_file():
                print(f"  - {file.name}")
        print("\nYou can view these online at: https://mermaid.live/")

if __name__ == "__main__":
    main()
