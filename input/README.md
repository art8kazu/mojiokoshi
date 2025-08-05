# 音声ファイル用ディレクトリ

このディレクトリに文字起こししたい音声ファイルを配置してください。

## 対応フォーマット
- MP3
- WAV  
- M4A
- FLAC
- AAC
- OGG
- WMA

## 使用例
```bash
# 単一ファイル
python transcriber.py input/meeting.mp3

# 高精度モード
python transcriber.py input/meeting.mp3 --model large-v3 --format continuous
```

**注意**: 音声ファイルや文字起こし結果ファイルは`.gitignore`で除外されるため、Gitで共有されません。