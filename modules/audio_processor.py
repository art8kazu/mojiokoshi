import whisper
import os
from datetime import timedelta
from typing import Dict, List, Optional
import re

class AudioProcessor:
    """音声処理クラス - Whisperを使用した文字起こし"""
    
    def __init__(self, model_name: str = "base", device: str = "cpu"):
        """
        初期化
        
        Args:
            model_name: Whisperモデル名 (tiny, base, small, medium, large, large-v2, large-v3)
            device: 使用デバイス (cpu, cuda, mps)
        """
        # モデル名の正規化
        if model_name == "large":
            model_name = "large-v3"  # 最新版を使用
            
        print(f"Whisperモデル '{model_name}' を読み込み中...")
        self.model = whisper.load_model(model_name, device=device)
        self.model_name = model_name
        self.device = device
        print("Whisperモデルの読み込み完了")
        
        # 日本語誤認識の修正パターン
        self.correction_patterns = [
            (r'八中', '発注'),
            (r'八乗っと', '発注ロット'),
            (r'インフォマト', 'インフォマート'),
            (r'インフマート', 'インフォマート'),
            (r'スクレッドシート', 'スプレッドシート'),
            (r'成球所', '請求書'),
            (r'悦子', 'えつこ'),
            (r'靖子', 'えつこ'),
        ]
    
    def transcribe(self, audio_path: str, language: str = "ja", 
                   enable_vad: bool = True, 
                   prompt: Optional[str] = None) -> Dict:
        """
        音声ファイルを文字起こし
        
        Args:
            audio_path: 音声ファイルのパス
            language: 言語コード (ja, en等)
            enable_vad: VAD (Voice Activity Detection) を有効にするか
            prompt: Whisperに与える初期プロンプト（文脈を提供）
            
        Returns:
            Whisperの結果辞書
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"音声ファイルが見つかりません: {audio_path}")
        
        print(f"音声ファイルを文字起こし中: {audio_path}")
        
        # Whisperで文字起こし実行（改善されたパラメータ）
        transcribe_params = {
            "language": language,
            "task": "transcribe",
            "word_timestamps": True,  # 単語レベルのタイムスタンプ
            "verbose": False,
            "temperature": 0.0,  # より決定的な出力のため
            "compression_ratio_threshold": 2.4,  # 圧縮率の閾値
            "logprob_threshold": -1.0,  # ログ確率の閾値
            "no_speech_threshold": 0.6,  # 無音検出の閾値
            "condition_on_previous_text": True,  # 前の文脈を考慮
        }
        
        # プロンプトがある場合のみ追加
        if prompt:
            transcribe_params["initial_prompt"] = prompt
            
        # VADは新しいwhisperバージョンでのみサポート（現在はスキップ）
        try:
            result = self.model.transcribe(audio_path, **transcribe_params)
        except TypeError as e:
            # パラメータが対応していない場合は基本的なパラメータのみで再実行
            print(f"一部のパラメータがサポートされていません。基本設定で実行します。")
            result = self.model.transcribe(
                audio_path,
                language=language,
                word_timestamps=True,
                verbose=False
            )
        
        # 後処理で誤認識を修正
        result = self._apply_corrections(result)
        
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
    
    def _apply_corrections(self, result: Dict) -> Dict:
        """
        日本語の誤認識を修正
        
        Args:
            result: Whisperの結果辞書
            
        Returns:
            修正後の結果辞書
        """
        # 全体テキストの修正
        if "text" in result:
            for pattern, replacement in self.correction_patterns:
                result["text"] = re.sub(pattern, replacement, result["text"])
        
        # 各セグメントの修正
        if "segments" in result:
            for segment in result["segments"]:
                if "text" in segment:
                    for pattern, replacement in self.correction_patterns:
                        segment["text"] = re.sub(pattern, replacement, segment["text"])
        
        return result
    
    def merge_segments(self, whisper_result: Dict, 
                      merge_threshold: float = 1.0,
                      max_segment_length: float = 30.0) -> List[Dict]:
        """
        短いセグメントを結合して、より自然な文章単位にする
        
        Args:
            whisper_result: Whisperの結果辞書
            merge_threshold: セグメント間の無音時間の閾値（秒）
            max_segment_length: 最大セグメント長（秒）
            
        Returns:
            結合されたセグメントのリスト
        """
        segments = whisper_result.get("segments", [])
        if not segments:
            return []
        
        merged_segments = []
        current_segment = {
            "start": segments[0]["start"],
            "end": segments[0]["end"],
            "text": segments[0]["text"].strip()
        }
        
        for i in range(1, len(segments)):
            segment = segments[i]
            silence_duration = segment["start"] - current_segment["end"]
            segment_duration = current_segment["end"] - current_segment["start"]
            
            # セグメントを結合するか判定
            should_merge = (
                silence_duration < merge_threshold and
                segment_duration < max_segment_length and
                not self._is_sentence_end(current_segment["text"])
            )
            
            if should_merge:
                # セグメントを結合
                current_segment["end"] = segment["end"]
                current_segment["text"] += segment["text"].strip()
            else:
                # 現在のセグメントを保存して新しいセグメントを開始
                merged_segments.append(current_segment)
                current_segment = {
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"].strip()
                }
        
        # 最後のセグメントを追加
        if current_segment:
            merged_segments.append(current_segment)
        
        return merged_segments
    
    def _is_sentence_end(self, text: str) -> bool:
        """
        文が終了しているかを判定
        
        Args:
            text: テキスト
            
        Returns:
            文が終了している場合True
        """
        sentence_endings = ['。', '！', '？', '.', '!', '?']
        return any(text.rstrip().endswith(ending) for ending in sentence_endings)
    
    def create_continuous_text(self, whisper_result: Dict, 
                             enable_timestamps: bool = False) -> str:
        """
        セグメントを結合して連続したテキストを生成
        
        Args:
            whisper_result: Whisperの結果辞書
            enable_timestamps: タイムスタンプを含めるか
            
        Returns:
            連続したテキスト
        """
        merged_segments = self.merge_segments(whisper_result)
        
        if enable_timestamps:
            text_lines = []
            for segment in merged_segments:
                start_time = self.format_timestamp(segment["start"])
                end_time = self.format_timestamp(segment["end"])
                text = segment["text"]
                text_lines.append(f"[{start_time} - {end_time}] {text}")
            return "\n".join(text_lines)
        else:
            # タイムスタンプなしの連続テキスト
            return "".join(segment["text"] for segment in merged_segments)