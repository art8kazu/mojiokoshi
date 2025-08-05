#!/bin/bash

# 文字起こし精度向上テストスクリプト

echo "========================================="
echo "文字起こし精度向上テスト"
echo "========================================="

# テスト対象ファイル
AUDIO_FILE="input/080525_etsuko.m4a"

# ファイル存在確認
if [ ! -f "$AUDIO_FILE" ]; then
    echo "エラー: 音声ファイルが見つかりません: $AUDIO_FILE"
    exit 1
fi

echo ""
echo "テスト1: 従来の設定（baseモデル）"
echo "-----------------------------------------"
python transcriber.py "$AUDIO_FILE" --model base --format standard

echo ""
echo "テスト2: 改善版（large-v3モデル + 連続テキスト）"
echo "-----------------------------------------"
python transcriber.py "$AUDIO_FILE" \
    --model large-v3 \
    --format continuous \
    --enable-vad \
    --prompt "日本語のビジネス会議。発注、請求書、インフォマート、スプレッドシートなどの業務用語を含む。"

echo ""
echo "========================================="
echo "テスト完了"
echo "outputディレクトリに結果が保存されました"
echo "========================================="