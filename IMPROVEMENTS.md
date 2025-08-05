# 文字起こしプログラムの精度向上改善

## 実装した改善内容

### 1. Whisperモデルのアップグレード
- `base`モデルから`large-v3`モデルへの対応を追加
- より高精度な文字起こしが可能に

### 2. セグメント結合機能
- 短い断片的なセグメントを自然な文章単位に結合
- 文脈を保持したより読みやすい出力

### 3. 日本語誤認識の自動修正
以下のような一般的な誤認識パターンを自動修正：
- 「八中」→「発注」
- 「八乗っと」→「発注ロット」
- 「インフォマト」→「インフォマート」
- 「スクレッドシート」→「スプレッドシート」
- 「成球所」→「請求書」

### 4. VAD（Voice Activity Detection）サポート
- 無音部分の検出と除去
- より効率的な処理と精度向上

### 5. 複数の出力形式
- `standard`: タイムスタンプ付きの標準形式
- `continuous`: タイムスタンプなしの連続テキスト形式
- `minimal`: 最小限のヘッダーで連続テキスト

## 使用方法

### 基本的な使用（従来通り）
```bash
python transcriber.py input/080525_etsuko.m4a
```

### 高精度モードで実行
```bash
# large-v3モデルを使用し、連続テキスト形式で出力
python transcriber.py input/080525_etsuko.m4a --model large-v3 --format continuous --enable-vad

# ビジネス会議の文脈を提供して精度向上
python transcriber.py input/080525_etsuko.m4a --model large-v3 --format continuous --prompt "ビジネス会議の議事録。インフォマート、スプレッドシート、発注などの業務用語を含む。"
```

### 推奨設定
最高の精度を得るために：
```bash
python transcriber.py input/080525_etsuko.m4a \
  --model large-v3 \
  --format continuous \
  --enable-vad \
  --prompt "日本語のビジネス会議。発注、請求書、スプレッドシートなどの業務用語を含む。" \
  --verbose
```

## 注意事項

### モデルサイズとメモリ使用量
- `tiny`: ~39MB (最速、精度低)
- `base`: ~74MB (バランス良好)
- `small`: ~244MB
- `medium`: ~769MB
- `large-v3`: ~1550MB (最高精度、処理時間長)

### 処理時間の目安
- `base`モデル: 約5分の音声で約5分
- `large-v3`モデル: 約5分の音声で約15-20分

### 推奨環境
- メモリ: 8GB以上（large-v3使用時は16GB推奨）
- GPU: 利用可能な場合は自動的に使用されます

## 環境設定（.env）

より高度な設定を行う場合は、`.env`ファイルを作成：

```bash
# Whisper設定
WHISPER_MODEL=large-v3
WHISPER_DEVICE=cpu  # GPUがある場合は "cuda" または "mps"(Mac)
WHISPER_LANGUAGE=ja

# 出力設定
OUTPUT_DIR=./output
OUTPUT_FORMAT=continuous
INCLUDE_TIMESTAMPS=false

# 処理設定
ENABLE_VAD=true
```

## トラブルシューティング

### メモリ不足エラー
large-v3モデルでメモリ不足が発生する場合：
1. より小さいモデル（medium）を使用
2. システムの仮想メモリを増やす
3. 他のアプリケーションを終了する

### 処理が遅い
1. GPUを利用する（CUDA対応GPUまたはApple Silicon Mac）
2. より小さいモデルを使用
3. 音声ファイルを短く分割して処理