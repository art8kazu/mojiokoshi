# ⚡ クイックスタートガイド

5分で始める音声文字起こし！

## 🎯 最速セットアップ（Mac）

```bash
# 1. 必要なツールをインストール
brew install python@3.11 ffmpeg git

# 2. アプリをダウンロード
cd ~/Desktop && git clone https://github.com/yourusername/mojiokoshi.git && cd mojiokoshi

# 3. セットアップスクリプトを実行
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# 4. 設定ファイルを準備
cp .env.example .env

# 5. APIキーを設定（DeepSeekが最安価でおすすめ）
echo "デスクトップの mojiokoshi/.env ファイルを開いてAPIキーを設定してください"
open .env

# 6. 実行！
python transcriber.py sample.mp3 --llm deepseek
```

## 🎯 最速セットアップ（Windows）

```cmd
:: 1. Pythonインストール後、コマンドプロンプトを管理者権限で開く

:: 2. デスクトップに移動してアプリをダウンロード
cd %USERPROFILE%\Desktop
git clone https://github.com/yourusername/mojiokoshi.git
cd mojiokoshi

:: 3. セットアップ
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

:: 4. 設定ファイルを準備
copy .env.example .env
notepad .env

:: 5. APIキーを設定して保存

:: 6. 実行！
python transcriber.py sample.mp3 --llm deepseek
```

## 🔑 APIキーの最速取得

### DeepSeek（推奨・最安価）
1. https://platform.deepseek.com/ にアクセス
2. 「Sign Up」でアカウント作成（メールアドレスのみ）
3. ダッシュボードから「API Keys」→「Create API Key」
4. キーをコピーして`.env`に貼り付け

**所要時間: 2分**

## 🚀 基本的な使い方

### シンプルな文字起こし（無料）
```bash
python transcriber.py meeting.mp3 --skip-llm
```

### 高精度文字起こし（推奨）
```bash
python transcriber.py meeting.mp3 --llm deepseek
```

### 複数ファイルを一括処理
```bash
python transcriber.py *.mp3 --batch --llm deepseek
```

## 💡 便利な使い方

### Mac: エイリアスを設定
```bash
echo 'alias moji="cd ~/Desktop/mojiokoshi && source venv/bin/activate && python transcriber.py"' >> ~/.zshrc
source ~/.zshrc

# 使用例
moji meeting.mp3 --llm deepseek
```

### Windows: ショートカット作成
デスクトップに `文字起こし.bat` を作成：
```batch
@echo off
cd /d %USERPROFILE%\Desktop\mojiokoshi
call venv\Scripts\activate
python transcriber.py %*
```

ファイルをドラッグ&ドロップで文字起こし！

## 📊 料金の目安

| 音声の長さ | Whisperのみ | + DeepSeek | + OpenAI |
|-----------|------------|-----------|----------|
| 10分 | 無料 | 約2円 | 約5円 |
| 30分 | 無料 | 約6円 | 約15円 |
| 60分 | 無料 | 約12円 | 約30円 |

## ❓ よくある質問

**Q: エラーが出ます**
```bash
# 仮想環境が有効か確認
# Mac: source venv/bin/activate
# Win: venv\Scripts\activate
```

**Q: 遅いです**
```bash
# 小さいモデルを使用
python transcriber.py audio.mp3 --model tiny
```

**Q: GPUを使いたい**
```bash
# .envファイルで設定
WHISPER_DEVICE=cuda  # NVIDIA
WHISPER_DEVICE=mps   # Mac M1/M2
```

## 🎉 完了！

これで高精度な音声文字起こしが使えます。
詳細は[README.md](README.md)をご覧ください。