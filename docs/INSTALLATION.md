# 🚀 インストールガイド

このガイドでは、Mac・Windows環境での「日本語会議記録文字起こしアプリ」のセットアップ手順を詳しく説明します。

## 📋 目次

1. [事前準備](#事前準備)
2. [Mac向けインストール手順](#mac向けインストール手順)
3. [Windows向けインストール手順](#windows向けインストール手順)
4. [共通設定](#共通設定)
5. [動作確認](#動作確認)
6. [トラブルシューティング](#トラブルシューティング)

---

## 事前準備

### 必要なもの
- インターネット接続
- 8GB以上のRAM推奨
- 5GB以上の空き容量
- 管理者権限

### APIキーの準備
以下のいずれか（または複数）のAPIキーを取得：

1. **DeepSeek（推奨・最安価）**
   - https://platform.deepseek.com/ でアカウント作成
   - APIキーを取得

2. **Google Gemini**
   - https://makersuite.google.com/app/apikey でAPIキー取得

3. **OpenAI**
   - https://platform.openai.com/api-keys でAPIキー取得

---

## Mac向けインストール手順

### 1. Homebrewのインストール（未インストールの場合）

Terminalを開いて以下を実行：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. 必要なソフトウェアのインストール

```bash
# Python 3.9以上のインストール
brew install python@3.11

# ffmpegのインストール（音声変換用）
brew install ffmpeg

# gitのインストール（未インストールの場合）
brew install git
```

### 3. アプリケーションのダウンロード

```bash
# 作業ディレクトリに移動
cd ~/Desktop

# リポジトリをクローン
git clone https://github.com/yourusername/mojiokoshi.git

# ディレクトリに移動
cd mojiokoshi
```

### 4. Python仮想環境の作成

```bash
# 仮想環境を作成
python3 -m venv venv

# 仮想環境を有効化
source venv/bin/activate

# pipをアップグレード
pip install --upgrade pip
```

### 5. 依存関係のインストール

```bash
# 必要なパッケージをインストール
pip install -r requirements.txt
```

### 6. 環境設定

```bash
# 環境変数ファイルをコピー
cp .env.example .env

# テキストエディタで.envを編集
nano .env
```

以下のようにAPIキーを設定：
```env
DEEPSEEK_API_KEY=your_actual_deepseek_key_here
GEMINI_API_KEY=your_actual_gemini_key_here
OPENAI_API_KEY=your_actual_openai_key_here
```

`Ctrl+X` → `Y` → `Enter` で保存して終了

### 7. エイリアスの設定（オプション）

```bash
# .zshrcまたは.bash_profileに追加
echo 'alias mojiokoshi="cd ~/Desktop/mojiokoshi && source venv/bin/activate && python transcriber.py"' >> ~/.zshrc

# 設定を反映
source ~/.zshrc
```

---

## Windows向けインストール手順

### 1. Python 3.11のインストール

1. https://www.python.org/downloads/ から最新のPython 3.11をダウンロード
2. インストーラーを実行
3. **重要**: 「Add Python to PATH」にチェックを入れる
4. 「Install Now」をクリック

### 2. ffmpegのインストール

1. https://www.gyan.dev/ffmpeg/builds/ にアクセス
2. 「release builds」の「full」版をダウンロード
3. ダウンロードしたZIPファイルを解凍
4. 解凍したフォルダを `C:\ffmpeg` に移動
5. システム環境変数のPATHに `C:\ffmpeg\bin` を追加：
   - Windowsキー + X → システム → システムの詳細設定
   - 環境変数 → Path → 編集 → 新規
   - `C:\ffmpeg\bin` を追加

### 3. Gitのインストール

1. https://git-scm.com/download/win からGit for Windowsをダウンロード
2. インストーラーを実行（デフォルト設定でOK）

### 4. コマンドプロンプトでの作業

**管理者権限でコマンドプロンプトを開く**：
- Windowsキー → 「cmd」と入力
- 「コマンドプロンプト」を右クリック → 「管理者として実行」

```cmd
# デスクトップに移動
cd %USERPROFILE%\Desktop

# リポジトリをクローン
git clone https://github.com/yourusername/mojiokoshi.git

# ディレクトリに移動
cd mojiokoshi
```

### 5. Python仮想環境の作成

```cmd
# 仮想環境を作成
python -m venv venv

# 仮想環境を有効化
venv\Scripts\activate

# pipをアップグレード
python -m pip install --upgrade pip
```

### 6. 依存関係のインストール

```cmd
# 必要なパッケージをインストール
pip install -r requirements.txt
```

### 7. 環境設定

```cmd
# 環境変数ファイルをコピー
copy .env.example .env

# メモ帳で編集
notepad .env
```

APIキーを設定して保存

### 8. ショートカットの作成（オプション）

デスクトップに `mojiokoshi.bat` を作成：

```batch
@echo off
cd /d C:\Users\%USERNAME%\Desktop\mojiokoshi
call venv\Scripts\activate
echo.
echo 音声文字起こしツール起動完了
echo 使用例: python transcriber.py audio.mp3
echo.
cmd /k
```

---

## 共通設定

### 推奨設定（.envファイル）

```env
# APIキー（最低1つは必須）
DEEPSEEK_API_KEY=your_deepseek_key
GEMINI_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key

# Whisper設定
WHISPER_MODEL=base  # 精度重視なら medium または large
WHISPER_DEVICE=cpu  # GPUがあれば cuda (Mac M1/M2は mps)

# デフォルトLLM
DEFAULT_LLM=deepseek  # 最もコスト効率が良い

# 出力設定
OUTPUT_DIR=./output
INCLUDE_TIMESTAMPS=true
```

### GPUを使用する場合（オプション）

**NVIDIA GPU（Windows/Linux）:**
```bash
# CUDA対応PyTorchをインストール
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**Apple Silicon（M1/M2 Mac）:**
```bash
# .envでデバイスを設定
WHISPER_DEVICE=mps
```

---

## 動作確認

### 1. インストール確認

```bash
# Mac/Linux
source venv/bin/activate  # 仮想環境を有効化

# Windows
venv\Scripts\activate

# 共通
python --version  # Python 3.9以上であることを確認
ffmpeg -version   # ffmpegがインストールされていることを確認
```

### 2. テスト実行

```bash
# ヘルプを表示
python transcriber.py --help

# サンプル音声で実行（音声ファイルを用意）
python transcriber.py sample.mp3 --skip-llm  # Whisperのみでテスト

# LLM処理も含めてテスト
python transcriber.py sample.mp3 --llm deepseek
```

### 3. 出力確認

```bash
# 出力ファイルを確認
# Mac/Linux
ls -la output/

# Windows
dir output
```

---

## トラブルシューティング

### よくある問題と解決方法

#### 1. "ModuleNotFoundError: No module named 'whisper'"

```bash
# 仮想環境が有効化されているか確認
# Mac/Linux
which python  # venv内のpythonを指しているか確認

# Windows
where python  # venv内のpython.exeを指しているか確認

# 再インストール
pip install --force-reinstall openai-whisper
```

#### 2. "ffmpeg not found"

**Mac:**
```bash
brew reinstall ffmpeg
```

**Windows:**
- 環境変数PATHに `C:\ffmpeg\bin` が含まれているか確認
- コマンドプロンプトを再起動

#### 3. メモリ不足エラー

`.env`ファイルで小さいモデルを使用：
```env
WHISPER_MODEL=tiny  # または base
```

#### 4. APIキーエラー

```bash
# 環境変数が正しく読み込まれているか確認
python -c "from modules.config import Config; print(Config.validate_api_keys())"
```

#### 5. 文字化け（Windows）

```python
# Windowsでの文字コード問題を解決
import sys
sys.stdout.reconfigure(encoding='utf-8')
```

### パフォーマンス最適化

#### GPU使用時の設定

```env
# .envファイル
WHISPER_MODEL=medium  # GPUなら大きいモデルも実用的
WHISPER_DEVICE=cuda   # NVIDIA GPU
# WHISPER_DEVICE=mps  # Apple Silicon
```

#### 長時間音声の処理

```env
# チャンクサイズを調整
CHUNK_LENGTH_SECONDS=300  # 5分ごとに分割
```

### サポート

問題が解決しない場合：
1. エラーメッセージ全文をコピー
2. 使用OS、Pythonバージョンを記載
3. GitHubのIssuesに投稿

---

## 🎉 セットアップ完了！

以下のコマンドで音声文字起こしを開始できます：

```bash
# 基本的な使用
python transcriber.py your_audio.mp3

# DeepSeekで後処理（推奨）
python transcriber.py your_audio.mp3 --llm deepseek

# 詳細は
python transcriber.py --help
```

楽しい文字起こしライフを！ 🎤📝