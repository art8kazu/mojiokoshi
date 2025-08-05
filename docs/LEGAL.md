# 📄 法的情報・ライセンス

## ソフトウェアライセンス

### 本アプリケーション
- **ライセンス**: MIT License
- **著作権**: Copyright (c) 2024 Japanese Meeting Transcription App
- **詳細**: [LICENSE](LICENSE) ファイルを参照

### 依存関係ライセンス

#### OpenAI Whisper
- **ライセンス**: MIT License
- **著作権**: Copyright (c) 2022 OpenAI
- **リポジトリ**: https://github.com/openai/whisper
- **用途**: 音声認識エンジン

#### その他の主要ライブラリ
| ライブラリ | ライセンス | 用途 |
|------------|------------|------|
| PyTorch | BSD-3-Clause | 機械学習フレームワーク |
| NumPy | BSD | 数値計算 |
| Requests | Apache 2.0 | HTTP通信 |
| Click | BSD-3-Clause | CLI構築 |
| python-dotenv | BSD-3-Clause | 環境変数管理 |

## モデルファイルについて

### Whisperモデル
- **配布**: 本アプリには含まれていません
- **取得方法**: 初回実行時にOpenAI公式サーバーから自動ダウンロード
- **保存場所**: `~/.cache/whisper/` (ユーザーのキャッシュディレクトリ)
- **ライセンス**: MIT License (OpenAI Whisper)

### 利用可能モデル
```
tiny.pt    (39MB)   - MIT License
base.pt    (74MB)   - MIT License  
small.pt   (244MB)  - MIT License
medium.pt  (769MB)  - MIT License
large-v3.pt(1550MB) - MIT License
```

## 商用利用について

### ✅ 許可されること
- **個人利用**: 無制限
- **商用利用**: 無制限
- **再配布**: ソースコード・バイナリ両方OK
- **改変**: 自由に改変・カスタマイズ可能
- **販売**: 改変版の販売も可能

### ⚠️ 条件
- MIT Licenseの表記を保持
- 著作権表示を保持
- 免責事項を保持

## APIサービスの利用規約

### LLM API
- **DeepSeek**: 各サービスの利用規約に従う
- **OpenAI**: OpenAI API利用規約に従う  
- **Google Gemini**: Google AI利用規約に従う

### 注意事項
- 本アプリの使用は無料ですが、LLM APIの利用には別途料金が発生します
- 各APIサービスの利用規約を必ず確認してください

## 免責事項

本ソフトウェアは「現状のまま」提供され、明示的または暗示的な保証は一切ありません。
使用によって生じるいかなる損害についても、作者は責任を負いません。

## サポート・お問い合わせ

- GitHub Issues: https://github.com/yourusername/mojiokoshi/issues
- ライセンスに関する質問: legal@yourdomain.com

---

最終更新: 2024年1月