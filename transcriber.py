#!/usr/bin/env python3
"""
高精度音声文字起こしアプリ
OpenAI Whisper + LLM後処理による日本語会議記録文字起こし
"""

import argparse
import time
import os
from modules.config import Config
from modules.audio_processor import AudioProcessor
from modules.llm_processor import LLMProcessor
from modules.output_formatter import OutputFormatter

def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(description="高精度音声文字起こしアプリ")
    parser.add_argument("audio_file", help="音声ファイルパス")
    parser.add_argument("--llm", choices=["deepseek", "gemini", "openai"], 
                       default="whisper", help="使用するLLM API (デフォルト: whisper only)")
    parser.add_argument("--model", default="base", 
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisperモデル (デフォルト: base)")
    parser.add_argument("--compare", action="store_true", 
                       help="複数APIで比較実行")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="詳細ログ出力")
    
    args = parser.parse_args()
    
    # 設定確認
    config = Config()
    available_apis = config.validate_api_keys()
    
    if args.verbose:
        print(f"利用可能なAPI: {available_apis}")
        print(f"Whisperモデル: {args.model}")
    
    # 音声ファイル存在確認
    if not os.path.exists(args.audio_file):
        print(f"エラー: 音声ファイルが見つかりません - {args.audio_file}")
        return
    
    try:
        # 音声処理器を初期化
        audio_processor = AudioProcessor(model_name=args.model)
        output_formatter = OutputFormatter(config.OUTPUT_DIR)
        
        # Whisperで文字起こし
        print("\n=== Whisper文字起こし開始 ===")
        start_time = time.time()
        
        whisper_result = audio_processor.transcribe(args.audio_file)
        timestamped_text = audio_processor.create_timestamped_text(whisper_result)
        
        whisper_time = time.time() - start_time
        print(f"Whisper処理時間: {whisper_time:.2f}秒")
        
        # Whisperのみの結果を保存
        metadata = {
            "whisper_model": args.model,
            "processing_time": whisper_time
        }
        
        whisper_output_path = output_formatter.save_transcription(
            timestamped_text, 
            args.audio_file, 
            "whisper",
            metadata
        )
        
        if args.verbose:
            print("\n=== Whisper結果プレビュー ===")
            preview = output_formatter.format_for_display(timestamped_text, 10)
            print(preview)
        
        print("\n=== 処理完了 ===")
        print(f"総処理時間: {time.time() - start_time:.2f}秒")
        
    except KeyboardInterrupt:
        print("\n処理が中断されました")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()