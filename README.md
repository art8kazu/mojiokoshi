# 🎤 日本語会議記録文字起こしアプリ

OpenAI Whisper + LLM後処理による高精度な日本語会議文字起こしツール

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## ✨ 特徴

- 🎯 **高精度**: Whisperによる初期文字起こし + LLMによる後処理で精度向上
- 🚀 **複数LLM対応**: DeepSeek、Gemini、OpenAIから選択可能
- 💰 **コスト比較**: 各LLMプロバイダーのコスト比較機能
- 📝 **複数フォーマット**: TXT、JSON、SRT、VTT形式での出力
- ⏱️ **タイムスタンプ付き**: 正確なタイムスタンプ付きテキスト出力
- 🔄 **バッチ処理**: 複数ファイルの一括処理対応

## 🚀 クイックスタート

### 超簡単セットアップ

**Mac/Linux:**
```bash
# 1分でセットアップ完了
curl -O https://raw.githubusercontent.com/yourusername/mojiokoshi/main/setup.sh
chmod +x setup.sh && ./setup.sh
```

**Windows:**
```cmd
REM setup.batをダウンロードして管理者権限で実行
setup.bat
```

### 手動インストール

詳細な手順は以下をご覧ください：
- 📖 [詳細インストールガイド](docs/INSTALLATION.md)
- ⚡ [クイックスタートガイド](docs/QUICKSTART.md)
- 📁 [プロジェクト構造](project_structure.md)

## 使用方法

### 基本的な使用
```bash
# 音声ファイルをinputフォルダに配置
cp meeting.mp3 input/

# 文字起こし実行
python transcriber.py input/meeting.mp3
```

### LLMプロバイダーを指定
```bash
python transcriber.py input/meeting.mp3 --llm deepseek
```

### 複数ファイルの処理
```bash
python transcriber.py input/*.mp3 --batch
```

### Whisperのみ（LLM処理をスキップ）
```bash
python transcriber.py input/meeting.mp3 --skip-llm
```

### コスト比較モード
```bash
python transcriber.py input/meeting.mp3 --compare-costs
```

### 詳細オプション
```bash
python transcriber.py input/meeting.mp3 \
  --llm gemini \
  --whisper-model medium \
  --device cuda \
  --format json \
  --save-intermediate \
  --verbose
```

## オプション一覧

| オプション | 説明 | デフォルト |
|------------|------|------------|
| `--llm` | LLMプロバイダー (deepseek/gemini/openai) | deepseek |
| `--skip-llm` | LLM後処理をスキップ | False |
| `--format` | 出力フォーマット (txt/json/srt/vtt) | txt |
| `--output-dir` | 出力ディレクトリ | ./output |
| `--config` | 設定ファイル（YAML） | - |
| `--whisper-model` | Whisperモデル (tiny/base/small/medium/large) | base |
| `--device` | 処理デバイス (cpu/cuda/mps) | cpu |
| `--batch` | バッチ処理モード | False |
| `--compare-costs` | コスト比較モード | False |
| `--save-intermediate` | 中間結果を保存 | False |
| `--verbose` | 詳細ログ出力 | False |
| `--log-file` | ログファイルパス | - |

## 設定ファイル

YAML形式の設定ファイルを使用可能：

```yaml
whisper:
  model: medium
  device: cuda
  language: ja

llm:
  default_provider: deepseek
  temperature: 0.3
  max_tokens: 4096

output:
  output_dir: ./results
  format: json
  include_timestamps: true

processing:
  batch_size: 10
  chunk_length_seconds: 600
  enable_vad: true
```

使用例：
```bash
python transcriber.py audio.mp3 --config config.yaml
```

## 出力例

### テキスト形式（タイムスタンプ付き）
```
[00:00:05] それでは、本日の会議を始めさせていただきます。
[00:00:12] まず、前回の議事録の確認から行いたいと思います。
[00:00:20] 山田さん、資料の共有をお願いできますでしょうか。
```

### JSON形式
```json
{
  "metadata": {
    "language": "ja",
    "duration": 1823.5,
    "segments_count": 145,
    "processed_at": "2024-01-15T10:30:00"
  },
  "segments": [
    {
      "id": 0,
      "start": 5.0,
      "end": 10.5,
      "text": "それでは、本日の会議を始めさせていただきます。"
    }
  ]
}
```

## コスト情報

各LLMプロバイダーの料金（1M トークンあたり）：

| プロバイダー | 入力 | 出力 |
|--------------|------|------|
| DeepSeek | $0.14 | $0.28 |
| Gemini 1.5 Flash | $0.075 | $0.30 |
| OpenAI GPT-4o-mini | $0.15 | $0.60 |

## トラブルシューティング

### Whisperモデルのダウンロードが遅い
初回実行時はモデルのダウンロードに時間がかかります。`WHISPER_MODEL_DIR`環境変数でキャッシュディレクトリを指定できます。

### CUDAが認識されない
PyTorchのCUDA対応バージョンをインストール：
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### メモリ不足エラー
- より小さいWhisperモデルを使用（`--whisper-model tiny`）
- チャンクサイズを調整（環境変数`CHUNK_LENGTH_SECONDS`）

## 📄 ライセンス

MIT License - 詳細は[LEGAL.md](LEGAL.md)をご覧ください

### 主要な依存関係
- **OpenAI Whisper**: MIT License
- **PyTorch**: BSD-3-Clause License
- **その他**: すべてオープンソース・商用利用可能

**商用利用・再配布・改変すべて自由です！**

## ⚠️ 免責事項・注意事項

### 利用上の責任について
- **本ソフトウェアは「現状のまま」提供されます**
- **利用者の責任において使用してください**
- 文字起こし結果の正確性は保証されません
- 機密情報や個人情報の取り扱いは利用者の責任です
- 本ツールの使用により生じたいかなる損害についても、開発者は責任を負いません

### セキュリティ・プライバシーに関する注意
- **機密性の高い音声ファイルの使用は推奨しません**
- LLM API使用時は、音声データがサードパーティに送信される可能性があります
- APIキーの管理は厳重に行ってください
- 重要な会議の場合は、事前にテスト実行を推奨します

### 推奨事項
- 重要な会議では複数の文字起こし手段を併用することを推奨
- 出力結果は必ず人間による確認・校正を行ってください
- 定期的にバックアップを取得してください

## 🤝 貢献

プルリクエスト歓迎です！詳細は[CONTRIBUTING.md](docs/CONTRIBUTING.md)をご覧ください。

- バグ報告: [Issues](https://github.com/yourusername/mojiokoshi/issues)
- 機能要望: [Issues](https://github.com/yourusername/mojiokoshi/issues)
- 開発参加: [Pull Requests](https://github.com/yourusername/mojiokoshi/pulls)