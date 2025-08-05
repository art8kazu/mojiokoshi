# 日本語会議記録文字起こしアプリ 要件定義・設計書

## 1. プロジェクト概要

### 目的
- 日本の会議音声ファイルを高精度で文字起こしするPythonアプリケーションの開発
- OpenAI Whisper + LLM後処理による精度向上
- タイムスタンプ付きプレーンテキスト出力

### 背景
- Google AI StudioやNotebook LMでの文字起こし精度に課題
- PLAUDE.aiレベルの高精度を目指す
- DeepSeek、Geminiなど安価で高性能なAPIを活用

## 2. 要件定義

### 2.1 機能要件

#### 基本機能
- [ ] 音声ファイル（mp3, wav, m4a等）の読み込み
- [ ] Whisperによる初期文字起こし
- [ ] LLMによる後処理（誤認識修正、句読点付与）
- [ ] タイムスタンプ付きテキスト出力
- [ ] ファイル保存機能

#### 高度な機能
- [ ] 複数LLM API対応（DeepSeek、Gemini、OpenAI）
- [ ] コスト比較機能
- [ ] バッチ処理対応
- [ ] 処理進捗表示

### 2.2 非機能要件

#### 性能要件
- 1時間の音声ファイルを20分以内で処理
- メモリ使用量は8GB以下
- 複数ファイルの並列処理対応

#### 品質要件
- 日本語会議記録に特化した精度向上
- エラーハンドリングの充実
- ログ出力機能

#### 使いやすさ要件
- コマンドライン引数による簡単操作
- 設定ファイルによるカスタマイズ
- 分かりやすい進捗表示

## 3. システム設計

### 3.1 アーキテクチャ概要

```
[音声ファイル] → [Whisper処理] → [LLM後処理] → [タイムスタンプ付きテキスト]
```

### 3.2 モジュール構成

#### 3.2.1 メインモジュール (`transcriber.py`)
- アプリケーションのエントリーポイント
- コマンドライン引数処理
- 処理フロー制御

#### 3.2.2 音声処理モジュール (`audio_processor.py`)
- Whisperモデル管理
- 音声ファイル読み込み
- 初期文字起こし処理
- タイムスタンプ生成

#### 3.2.3 LLM処理モジュール (`llm_processor.py`)
- 各種LLM APIクライアント
- プロンプト管理
- 後処理ロジック
- エラーハンドリング

#### 3.2.4 出力処理モジュール (`output_formatter.py`)
- テキスト整形
- ファイル出力
- フォーマット変換

#### 3.2.5 設定管理モジュール (`config.py`)
- 環境変数管理
- 設定ファイル読み込み
- デフォルト値定義

### 3.3 データフロー

1. **入力**: 音声ファイルパス、設定パラメータ
2. **Whisper処理**: 音声 → セグメント化されたテキスト + タイムスタンプ
3. **LLM後処理**: 生テキスト → 校正されたテキスト
4. **出力**: タイムスタンプ付き最終テキスト

### 3.4 API設計

#### 3.4.1 LLMプロンプト設計

```python
IMPROVEMENT_PROMPT = """
以下は日本の会議音声をWhisperで文字起こしした結果です。
会議記録として適切になるよう、以下の点を修正してください：

1. 音声認識の誤認識を修正
2. 適切な句読点・改行を追加
3. 話し言葉を自然な書き言葉に調整
4. 専門用語・固有名詞の正確性確保
5. タイムスタンプ形式は保持

【修正対象テキスト】
{raw_text}

【修正後テキスト】
"""
```

#### 3.4.2 各LLM APIクライアント仕様

**DeepSeek API**
- エンドポイント: `https://api.deepseek.com/v1/chat/completions`
- モデル: `deepseek-chat`
- 料金: 約$0.14/1M tokens

**Gemini API**
- エンドポイント: Google AI Studio API
- モデル: `gemini-1.5-flash`
- 料金: 約$0.075/1M tokens

**OpenAI API**
- エンドポイント: `https://api.openai.com/v1/chat/completions`
- モデル: `gpt-4o-mini`
- 料金: 約$0.15/1M tokens

## 4. 実装タスクリスト

### Phase 1: 基盤実装
- [ ] プロジェクト環境構築
  - [ ] requirements.txt作成
  - [ ] .env.example作成
  - [ ] 基本ディレクトリ構造作成
  
- [ ] 設定管理実装
  - [ ] config.py実装
  - [ ] 環境変数読み込み機能
  - [ ] 設定値バリデーション

### Phase 2: 音声処理実装
- [ ] audio_processor.py実装
  - [ ] Whisperモデル初期化
  - [ ] 音声ファイル読み込み
  - [ ] 文字起こし処理
  - [ ] タイムスタンプ生成
  - [ ] セグメント分割

### Phase 3: LLM処理実装
- [ ] llm_processor.py実装
  - [ ] DeepSeek APIクライアント
  - [ ] Gemini APIクライアント
  - [ ] OpenAI APIクライアント
  - [ ] プロンプト管理
  - [ ] エラーハンドリング
  - [ ] レート制限対応

### Phase 4: 出力処理実装
- [ ] output_formatter.py実装
  - [ ] タイムスタンプフォーマット
  - [ ] テキスト整形
  - [ ] ファイル出力
  - [ ] 複数フォーマット対応

### Phase 5: メイン処理実装
- [ ] transcriber.py実装
  - [ ] コマンドライン引数処理
  - [ ] メイン処理フロー
  - [ ] 進捗表示
  - [ ] ログ出力
  - [ ] エラーハンドリング

### Phase 6: 機能拡張
- [ ] バッチ処理機能
- [ ] コスト計算機能
- [ ] 複数API比較機能
- [ ] 設定ファイル対応

### Phase 7: テスト・最適化
- [ ] 単体テスト作成
- [ ] 統合テスト実行
- [ ] 性能最適化
- [ ] ドキュメント整備

## 5. ファイル構成

```
mojiokoshi/
├── requirements.txt              # 依存関係
├── .env.example                 # 環境変数サンプル
├── README.md                    # 使用方法説明
├── transcriber.py              # メインスクリプト
├── modules/
│   ├── __init__.py
│   ├── audio_processor.py      # 音声処理
│   ├── llm_processor.py        # LLM処理
│   ├── output_formatter.py     # 出力処理
│   └── config.py              # 設定管理
├── prompts/
│   └── improvement_prompt.txt  # LLMプロンプト
├── output/                     # 出力ファイル格納
├── logs/                       # ログファイル
└── tests/                      # テストファイル
```

## 6. 使用例

```bash
# 基本的な使用方法
python transcriber.py input.mp3

# LLM指定
python transcriber.py input.mp3 --llm deepseek

# 複数ファイル処理
python transcriber.py *.mp3 --batch

# 詳細ログ出力
python transcriber.py input.mp3 --verbose

# コスト比較モード
python transcriber.py input.mp3 --compare-costs
```

## 7. 環境設定

### 必要な環境変数
```env
# .env ファイル
OPENAI_API_KEY=your_openai_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
GEMINI_API_KEY=your_gemini_api_key

# Whisper設定
WHISPER_MODEL=base  # tiny, base, small, medium, large
WHISPER_DEVICE=cpu  # cpu, cuda

# 出力設定
OUTPUT_DIR=./output
LOG_LEVEL=INFO
```

## 8. 実装優先度

1. **最優先**: Phase 1-2 (基盤・音声処理)
2. **高優先**: Phase 3-4 (LLM・出力処理)
3. **中優先**: Phase 5 (メイン処理)
4. **低優先**: Phase 6-7 (拡張・最適化)

## 9. 技術的考慮事項

### セキュリティ
- API キーの安全な管理
- 音声ファイルの一時的な取り扱い
- ログファイルでの機密情報除外

### パフォーマンス
- Whisperモデルサイズの選択
- メモリ使用量の最適化
- 並列処理の実装

### エラー処理
- ネットワークエラー対応
- API制限エラー対応
- ファイル読み込みエラー対応

## 10. 成功指標

- 文字起こし精度: Whisper単体比で20%以上向上
- 処理速度: 1時間音声を20分以内で処理
- コスト効率: 1時間音声あたり$0.50以下
- 使いやすさ: ワンコマンドで実行可能

---

この設計書を基に、Claude Codeに各フェーズを順次実装してもらってください。