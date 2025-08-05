#!/bin/bash
# 自動セットアップスクリプト（Mac/Linux用）

set -e

echo "🎤 日本語会議記録文字起こしアプリ セットアップスクリプト"
echo "================================================"

# カラー設定
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# OS判定
OS="Unknown"
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="Mac"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
fi

echo "検出されたOS: $OS"
echo ""

# 1. 依存関係チェック
echo "📋 依存関係をチェック中..."

# Python チェック
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION が見つかりました"
    
    # バージョンチェック
    REQUIRED_VERSION="3.9"
    if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
        echo -e "${RED}✗${NC} Python 3.9以上が必要です"
        exit 1
    fi
else
    echo -e "${RED}✗${NC} Pythonが見つかりません"
    if [[ "$OS" == "Mac" ]]; then
        echo "  Homebrewでインストール: brew install python@3.11"
    else
        echo "  パッケージマネージャーでPython 3.9以上をインストールしてください"
    fi
    exit 1
fi

# ffmpeg チェック
if command -v ffmpeg &> /dev/null; then
    echo -e "${GREEN}✓${NC} ffmpegが見つかりました"
else
    echo -e "${YELLOW}!${NC} ffmpegが見つかりません"
    if [[ "$OS" == "Mac" ]]; then
        echo "  インストールしますか？ (y/n)"
        read -r response
        if [[ "$response" =~ ^[Yy]$ ]]; then
            brew install ffmpeg
        else
            echo "  後で手動でインストール: brew install ffmpeg"
        fi
    else
        echo "  パッケージマネージャーでffmpegをインストールしてください"
    fi
fi

echo ""

# 2. 仮想環境セットアップ
echo "🔧 Python仮想環境をセットアップ中..."

if [ -d "venv" ]; then
    echo "  既存の仮想環境が見つかりました"
else
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} 仮想環境を作成しました"
fi

# 仮想環境を有効化
source venv/bin/activate

# pipアップグレード
pip install --upgrade pip -q
echo -e "${GREEN}✓${NC} pipをアップグレードしました"

echo ""

# 3. 依存関係インストール
echo "📦 依存関係をインストール中..."
pip install -r requirements.txt
echo -e "${GREEN}✓${NC} 必要なパッケージをインストールしました"

echo ""

# 4. 環境設定
echo "⚙️  環境設定..."

if [ -f ".env" ]; then
    echo "  .envファイルが既に存在します"
else
    cp .env.example .env
    echo -e "${GREEN}✓${NC} .envファイルを作成しました"
fi

echo ""

# 5. APIキー設定確認
echo "🔑 APIキー設定"
echo "  .envファイルを編集してAPIキーを設定してください:"
echo ""
echo "  1. DeepSeek (推奨・最安価): https://platform.deepseek.com/"
echo "  2. Google Gemini: https://makersuite.google.com/app/apikey"
echo "  3. OpenAI: https://platform.openai.com/api-keys"
echo ""

# .envファイルを開くか確認
echo "  .envファイルを今開きますか？ (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    if [[ "$OS" == "Mac" ]]; then
        open .env
    else
        ${EDITOR:-nano} .env
    fi
fi

echo ""

# 6. エイリアス設定（オプション）
echo "🚀 エイリアス設定（オプション）"
echo "  'moji'コマンドでアプリを簡単に起動できるようにしますか？ (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    SHELL_RC=""
    if [ -f "$HOME/.zshrc" ]; then
        SHELL_RC="$HOME/.zshrc"
    elif [ -f "$HOME/.bashrc" ]; then
        SHELL_RC="$HOME/.bashrc"
    fi
    
    if [ -n "$SHELL_RC" ]; then
        ALIAS_CMD="alias moji='cd $(pwd) && source venv/bin/activate && python transcriber.py'"
        if ! grep -q "alias moji=" "$SHELL_RC"; then
            echo "$ALIAS_CMD" >> "$SHELL_RC"
            echo -e "${GREEN}✓${NC} エイリアスを設定しました"
            echo "  新しいターミナルで 'moji audio.mp3' のように使用できます"
        else
            echo "  エイリアスは既に設定されています"
        fi
    fi
fi

echo ""

# 7. 動作テスト
echo "🧪 動作テスト"
echo "  セットアップが正しく完了したか確認します..."

# インポートテスト
if python -c "import whisper, openai, requests" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} 必要なモジュールが正しくインポートできます"
else
    echo -e "${RED}✗${NC} モジュールのインポートに失敗しました"
    exit 1
fi

# API設定確認
API_CHECK=$(python -c "from modules.config import Config; apis = Config.validate_api_keys(); print(len(apis))" 2>/dev/null || echo "0")
if [ "$API_CHECK" -gt 0 ]; then
    echo -e "${GREEN}✓${NC} $API_CHECK 個のAPIキーが設定されています"
else
    echo -e "${YELLOW}!${NC} APIキーが設定されていません"
    echo "    .envファイルを編集してAPIキーを設定してください"
fi

echo ""

# 8. 完了メッセージ
echo "================================================"
echo -e "${GREEN}✅ セットアップが完了しました！${NC}"
echo ""
echo "📝 使い方:"
echo "  # 基本的な使用（Whisperのみ）"
echo "  python transcriber.py audio.mp3 --skip-llm"
echo ""
echo "  # LLM後処理あり（推奨）"
echo "  python transcriber.py audio.mp3 --llm deepseek"
echo ""
echo "  # ヘルプを表示"
echo "  python transcriber.py --help"
echo ""

if [ "$API_CHECK" -eq 0 ]; then
    echo -e "${YELLOW}⚠️  注意: APIキーを設定してからLLM機能を使用してください${NC}"
fi

echo ""
echo "詳細は README.md をご覧ください"
echo "================================================"