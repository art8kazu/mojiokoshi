# 🎤 サンプル音声ファイル

テスト用のサンプル音声ファイルを配置するディレクトリです。

## サンプルファイルの取得

### 1. 自分で録音
```bash
# macOS
say "こんにちは、これはテスト用の音声です。今日は良い天気ですね。" -o samples/test_ja.aiff

# Windows (PowerShell)
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.Speak("This is a test audio file")
```

### 2. オンラインサンプル
以下のサイトから日本語音声サンプルをダウンロード：
- [音声合成サービス](https://www.text-to-speech.jp/)
- [フリー音声素材](https://on-jin.com/)

### 3. テスト実行
```bash
# Whisperのみでテスト
python transcriber.py samples/test.mp3 --skip-llm

# LLM後処理込みでテスト  
python transcriber.py samples/test.mp3 --llm deepseek
```

## 推奨サンプル内容

日本語会議を想定した内容：
- 挨拶・自己紹介
- 数字・日付（売上、期日など）
- 専門用語・固有名詞
- 質疑応答形式

例：
> 皆様、おはようございます。本日は第3四半期の業績報告をさせていただきます。
> 売上高は前年同期比で15%増の120億円となりました。
> これは主に新製品「AIアシスタント」の好調な売れ行きによるものです。