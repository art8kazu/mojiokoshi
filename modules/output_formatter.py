import os
from datetime import datetime
from typing import Dict

class OutputFormatter:
    """出力処理クラス - テキスト整形とファイル出力"""
    
    def __init__(self, output_dir: str = "./output"):
        """
        初期化
        
        Args:
            output_dir: 出力ディレクトリ
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def save_transcription(self, 
                          text: str, 
                          audio_filename: str, 
                          api_used: str = "whisper",
                          metadata: Dict = None) -> str:
        """
        文字起こし結果をファイルに保存
        
        Args:
            text: 文字起こしテキスト
            audio_filename: 元の音声ファイル名
            api_used: 使用したAPI名
            metadata: メタデータ辞書
            
        Returns:
            保存されたファイルのパス
        """
        # 出力ファイル名を生成
        base_name = os.path.splitext(os.path.basename(audio_filename))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{base_name}_{api_used}_{timestamp}.txt"
        output_path = os.path.join(self.output_dir, output_filename)
        
        # ヘッダー情報を作成
        header = self._create_header(audio_filename, api_used, metadata)
        
        # ファイルに保存
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(header)
            f.write("\n" + "="*80 + "\n")
            f.write("文字起こし結果\n")
            f.write("="*80 + "\n\n")
            f.write(text)
        
        print(f"文字起こし結果を保存しました: {output_path}")
        return output_path
    
    def _create_header(self, audio_filename: str, api_used: str, metadata: Dict = None) -> str:
        """ファイルヘッダーを作成"""
        header = f"""# 音声文字起こし結果

## 処理情報
- 音声ファイル: {audio_filename}
- 処理日時: {datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")}
- 使用API: {api_used}
"""
        
        if metadata:
            header += f"- Whisperモデル: {metadata.get('whisper_model', 'unknown')}\n"
            header += f"- 処理時間: {metadata.get('processing_time', 'unknown')}秒\n"
            if 'estimated_cost' in metadata:
                header += f"- 推定コスト: ${metadata['estimated_cost']:.4f}\n"
        
        return header
    
    def create_comparison_report(self, results: Dict[str, str], audio_filename: str) -> str:
        """
        複数API結果の比較レポートを作成
        
        Args:
            results: API名をキーとした結果辞書
            audio_filename: 元の音声ファイル名
            
        Returns:
            保存されたレポートファイルのパス
        """
        base_name = os.path.splitext(os.path.basename(audio_filename))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"{base_name}_comparison_{timestamp}.txt"
        report_path = os.path.join(self.output_dir, report_filename)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"# 文字起こし比較レポート\n\n")
            f.write(f"音声ファイル: {audio_filename}\n")
            f.write(f"処理日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}\n\n")
            
            for api_name, result_text in results.items():
                f.write(f"## {api_name.upper()} 結果\n")
                f.write("="*60 + "\n")
                f.write(result_text)
                f.write("\n\n")
        
        print(f"比較レポートを保存しました: {report_path}")
        return report_path
    
    def format_for_display(self, text: str, max_lines: int = 20) -> str:
        """
        表示用にテキストを整形
        
        Args:
            text: 整形するテキスト
            max_lines: 表示する最大行数
            
        Returns:
            整形されたテキスト
        """
        lines = text.split('\n')
        
        if len(lines) <= max_lines:
            return text
        
        # 先頭部分と末尾部分を表示
        head_lines = lines[:max_lines//2]
        tail_lines = lines[-(max_lines//2):]
        
        return '\n'.join(head_lines) + f'\n\n... ({len(lines) - max_lines}行省略) ...\n\n' + '\n'.join(tail_lines)