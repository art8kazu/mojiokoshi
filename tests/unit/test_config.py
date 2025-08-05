"""
Configuration module unit tests
"""

import pytest
import os
from pathlib import Path
from modules.config import Config


class TestConfig:
    """Configuration tests"""
    
    def test_default_values(self):
        """Test default configuration values"""
        config = Config()
        
        assert config.WHISPER_MODEL == "base"
        assert config.WHISPER_DEVICE == "cpu"
        assert config.OUTPUT_DIR == "./output"
        assert config.LOG_LEVEL == "INFO"
    
    def test_api_key_validation(self):
        """Test API key validation"""
        # Mock environment variables
        original_deepseek = os.environ.get("DEEPSEEK_API_KEY")
        original_openai = os.environ.get("OPENAI_API_KEY")
        
        try:
            # Test with no API keys
            os.environ.pop("DEEPSEEK_API_KEY", None)
            os.environ.pop("OPENAI_API_KEY", None)
            
            available_apis = Config.validate_api_keys()
            assert len(available_apis) == 0
            
            # Test with DeepSeek key
            os.environ["DEEPSEEK_API_KEY"] = "test_key"
            available_apis = Config.validate_api_keys()
            assert "deepseek" in available_apis
            
        finally:
            # Restore original environment
            if original_deepseek:
                os.environ["DEEPSEEK_API_KEY"] = original_deepseek
            if original_openai:
                os.environ["OPENAI_API_KEY"] = original_openai