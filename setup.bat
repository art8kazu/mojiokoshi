@echo off
REM 自動セットアップスクリプト（Windows用）
setlocal enabledelayedexpansion

echo.
echo 🎤 日本語会議記録文字起こしアプリ セットアップスクリプト
echo ================================================
echo.

REM 管理者権限チェック
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ このスクリプトは管理者権限で実行してください
    echo    右クリック → "管理者として実行"
    pause
    exit /b 1
)

REM 1. 依存関係チェック
echo 📋 依存関係をチェック中...

REM Python チェック
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ Pythonが見つかりません
    echo    https://www.python.org/downloads/ からPython 3.9以上をインストールしてください
    echo    インストール時に "Add Python to PATH" にチェックを入れてください
    pause
    exit /b 1
) else (
    for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
    echo ✅ Python !PYTHON_VERSION! が見つかりました
)

REM ffmpeg チェック
ffmpeg -version >nul 2>&1
if %errorLevel% neq 0 (
    echo ⚠️  ffmpegが見つかりません
    echo    以下の手順でインストールしてください:
    echo    1. https://www.gyan.dev/ffmpeg/builds/ からダウンロード
    echo    2. C:\ffmpeg に解凍
    echo    3. 環境変数PATHに C:\ffmpeg\bin を追加
    echo.
    echo    続行しますか？ ^(y/n^)
    set /p response=
    if /i not "!response!"=="y" (
        echo セットアップを中止しました
        pause
        exit /b 1
    )
) else (
    echo ✅ ffmpegが見つかりました
)

echo.

REM 2. 仮想環境セットアップ
echo 🔧 Python仮想環境をセットアップ中...

if exist "venv" (
    echo   既存の仮想環境が見つかりました
) else (
    python -m venv venv
    if %errorLevel% neq 0 (
        echo ❌ 仮想環境の作成に失敗しました
        pause
        exit /b 1
    )
    echo ✅ 仮想環境を作成しました
)

REM 仮想環境を有効化
call venv\Scripts\activate
if %errorLevel% neq 0 (
    echo ❌ 仮想環境の有効化に失敗しました
    pause
    exit /b 1
)

REM pipアップグレード
echo   pipをアップグレード中...
python -m pip install --upgrade pip >nul 2>&1
echo ✅ pipをアップグレードしました

echo.

REM 3. 依存関係インストール
echo 📦 依存関係をインストール中...
echo   これには数分かかる場合があります...

pip install -r requirements.txt
if %errorLevel% neq 0 (
    echo ❌ パッケージのインストールに失敗しました
    pause
    exit /b 1
)
echo ✅ 必要なパッケージをインストールしました

echo.

REM 4. 環境設定
echo ⚙️  環境設定...

if exist ".env" (
    echo   .envファイルが既に存在します
) else (
    copy ".env.example" ".env" >nul
    echo ✅ .envファイルを作成しました
)

echo.

REM 5. APIキー設定
echo 🔑 APIキー設定
echo   .envファイルを編集してAPIキーを設定してください:
echo.
echo   1. DeepSeek ^(推奨・最安価^): https://platform.deepseek.com/
echo   2. Google Gemini: https://makersuite.google.com/app/apikey
echo   3. OpenAI: https://platform.openai.com/api-keys
echo.

echo   .envファイルを今開きますか？ ^(y/n^)
set /p response=
if /i "!response!"=="y" (
    notepad .env
)

echo.

REM 6. ショートカット作成（オプション）
echo 🚀 ショートカット作成^(オプション^)
echo   デスクトップにショートカットを作成しますか？ ^(y/n^)
set /p response=
if /i "!response!"=="y" (
    set CURRENT_DIR=%cd%
    set SHORTCUT_PATH=%USERPROFILE%\Desktop\文字起こし.bat
    
    echo @echo off > "!SHORTCUT_PATH!"
    echo cd /d "!CURRENT_DIR!" >> "!SHORTCUT_PATH!"
    echo call venv\Scripts\activate >> "!SHORTCUT_PATH!"
    echo echo. >> "!SHORTCUT_PATH!"
    echo echo 音声文字起こしツール >> "!SHORTCUT_PATH!"
    echo echo 使用例: python transcriber.py audio.mp3 --llm deepseek >> "!SHORTCUT_PATH!"
    echo echo. >> "!SHORTCUT_PATH!"
    echo cmd /k >> "!SHORTCUT_PATH!"
    
    echo ✅ デスクトップにショートカットを作成しました
)

echo.

REM 7. 動作テスト
echo 🧪 動作テスト
echo   セットアップが正しく完了したか確認します...

REM インポートテスト
python -c "import whisper, openai, requests" >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ 必要なモジュールのインポートに失敗しました
    pause
    exit /b 1
) else (
    echo ✅ 必要なモジュールが正しくインポートできます
)

REM API設定確認
for /f %%i in ('python -c "from modules.config import Config; print(len(Config.validate_api_keys()))" 2^>nul') do set API_COUNT=%%i
if "!API_COUNT!"=="0" (
    echo ⚠️  APIキーが設定されていません
    echo     .envファイルを編集してAPIキーを設定してください
) else (
    echo ✅ !API_COUNT! 個のAPIキーが設定されています
)

echo.

REM 8. 完了メッセージ
echo ================================================
echo ✅ セットアップが完了しました！
echo.
echo 📝 使い方:
echo   # 基本的な使用^(Whisperのみ^)
echo   python transcriber.py audio.mp3 --skip-llm
echo.
echo   # LLM後処理あり^(推奨^)
echo   python transcriber.py audio.mp3 --llm deepseek
echo.
echo   # ヘルプを表示
echo   python transcriber.py --help
echo.

if "!API_COUNT!"=="0" (
    echo ⚠️  注意: APIキーを設定してからLLM機能を使用してください
)

echo.
echo 詳細は README.md をご覧ください
echo ================================================

pause