import whisper
import os
from datetime import timedelta
from typing import Dict, List

class AudioProcessor:
    """音声処理クラス - Whisperを使用した文字起こし"""
    
    def __init__(self, model_name: str = "base", device: str = "cpu"):
        """
        初期化
        
        Args:
            model_name: Whisperモデル名 (tiny, base, small, medium, large)
            device: 使用デバイス (cpu, cuda)
        """
        print(f"Whisperモデル '{model_name}' を読み込み中...")
        self.model = whisper.load_model(model_name, device=device)
        self.model_name = model_name
        self.device = device
        print("Whisperモデルの読み込み完了")
    
    def transcribe(self, audio_path: str, language: str = "ja") -> Dict:
        """
        音声ファイルを文字起こし
        
        Args:
            audio_path: 音声ファイルのパス
            language: 言語コード (ja, en等)
            
        Returns:
            Whisperの結果辞書
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"音声ファイルが見つかりません: {audio_path}")
        
        print(f"音声ファイルを文字起こし中: {audio_path}")
        
        # Whisperで文字起こし実行
        result = self.model.transcribe(
            audio_path,
            language=language,
            task="transcribe",
            word_timestamps=True,  # 単語レベルのタイムスタンプ
            verbose=False
        )
        
        print(f"文字起こし完了 - {len(result['segments'])}個のセグメント")
        return result
    
    def format_timestamp(self, seconds: float) -> str:
        """
        秒をHH:MM:SS形式に変換
        
        Args:
            seconds: 秒数
            
        Returns:
            HH:MM:SS形式の時刻文字列
        """
        td = timedelta(seconds=seconds)
        hours, remainder = divmod(td.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
    
    def create_timestamped_text(self, whisper_result: Dict) -> str:
        """
        Whisperの結果からタイムスタンプ付きテキストを生成
        
        Args:
            whisper_result: Whisperの結果辞書
            
        Returns:
            タイムスタンプ付きテキスト
        """
        timestamped_text = ""
        
        for segment in whisper_result["segments"]:
            start_time = self.format_timestamp(segment["start"])
            end_time = self.format_timestamp(segment["end"])
            text = segment["text"].strip()
            
            timestamped_text += f"[{start_time} - {end_time}] {text}\n"
        
        return timestamped_text
    
    def get_plain_text(self, whisper_result: Dict) -> str:
        """
        Whisperの結果からプレーンテキストを取得
        
        Args:
            whisper_result: Whisperの結果辞書
            
        Returns:
            プレーンテキスト
        """
        return whisper_result.get("text", "").strip()