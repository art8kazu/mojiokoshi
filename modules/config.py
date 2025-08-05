import os
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

class Config:
    """設定管理クラス"""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY") 
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Whisper設定
    WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")
    WHISPER_DEVICE = os.getenv("WHISPER_DEVICE", "cpu")
    
    # 出力設定
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./output")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # API URLs
    DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
    OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
    
    @classmethod
    def validate_api_keys(cls):
        """APIキーの存在確認"""
        available_apis = []
        if cls.OPENAI_API_KEY:
            available_apis.append("openai")
        if cls.DEEPSEEK_API_KEY:
            available_apis.append("deepseek")
        if cls.GEMINI_API_KEY:
            available_apis.append("gemini")
        return available_apis