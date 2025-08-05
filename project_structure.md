# 📁 プロジェクト構造

整理されたディレクトリ構造の説明

```
mojiokoshi/
├── 📄 README.md                    # メイン説明書
├── 📄 LICENSE                      # MITライセンス
├── ⚙️ requirements.txt             # Python依存関係
├── ⚙️ .env.example                 # 環境変数テンプレート
├── 🚀 transcriber.py               # メインアプリケーション
├── 🔧 setup.sh                     # Mac/Linux自動セットアップ
├── 🔧 setup.bat                    # Windows自動セットアップ
├── 📊 transcription_project_spec.md # 設計仕様書
│
├── 📂 modules/                     # アプリケーションモジュール
│   ├── __init__.py
│   ├── config.py                   # 設定管理
│   ├── audio_processor.py          # Whisper音声処理
│   ├── llm_processor.py            # LLM後処理
│   ├── output_formatter.py         # 出力フォーマット
│   └── improvement_prompt.txt      # LLMプロンプト
│
├── 📂 input/                       # 📥 音声ファイル配置場所
│   └── .gitkeep                    # (ここに音声ファイルを配置)
│
├── 📂 output/                      # 📤 文字起こし結果
│   └── .gitkeep                    # (結果ファイルが出力される)
│
├── 📂 samples/                     # 🎤 サンプル音声ファイル
│   └── README.md                   # サンプル取得方法
│
├── 📂 logs/                        # 📋 ログファイル
│   └── .gitkeep
│
├── 📂 docs/                        # 📚 詳細ドキュメント
│   ├── INSTALLATION.md             # インストール手順
│   ├── QUICKSTART.md               # クイックスタート
│   ├── CONTRIBUTING.md             # 開発者ガイド
│   └── LEGAL.md                    # ライセンス詳細
│
├── 📂 tests/                       # 🧪 テストファイル
│   ├── __init__.py
│   ├── unit/                       # ユニットテスト
│   │   ├── __init__.py
│   │   └── test_config.py
│   └── integration/                # 統合テスト
│
└── 📂 .github/                     # GitHub設定
    └── workflows/
        └── ci.yml                  # CI/CDパイプライン
```

## 📋 ディレクトリ説明

### 🎯 ユーザー操作
- **`input/`** - 音声ファイルを配置
- **`output/`** - 結果ファイルが出力
- **`samples/`** - テスト用サンプル

### ⚙️ アプリケーション
- **`modules/`** - 核となるPythonモジュール
- **`transcriber.py`** - メインエントリーポイント

### 📚 ドキュメント
- **`docs/`** - 詳細ドキュメント集
- **`README.md`** - メイン説明

### 🔧 開発者向け
- **`tests/`** - テストコード
- **`.github/`** - CI/CD設定

## 🚀 使い方

### 基本的な使用
```bash
# 1. 音声ファイルをinputディレクトリに配置
cp meeting.mp3 input/

# 2. 文字起こし実行
python transcriber.py input/meeting.mp3 --llm deepseek

# 3. 結果をoutputディレクトリで確認
ls output/
```

### バッチ処理
```bash
# inputディレクトリの全ファイルを処理
python transcriber.py input/*.mp3 --batch --llm deepseek
```

## 🎯 設計思想

1. **明確な役割分担**: 入力・出力・処理を明確に分離
2. **使いやすさ**: ユーザーが迷わないシンプルな構造
3. **開発しやすさ**: モジュール化・テスト・CI完備
4. **公開準備**: ドキュメント・ライセンス完備