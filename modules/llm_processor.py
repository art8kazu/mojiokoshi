import requests
import json
import openai
from typing import Optional
from .config import Config

class LLMProcessor:
    """LLM処理クラス - 各種LLM APIを使用した文字起こし後処理"""
    
    def __init__(self):
        """初期化"""
        self.config = Config()
        self.available_apis = Config.validate_api_keys()
        print(f"利用可能なAPI: {', '.join(self.available_apis)}")
    
    def improve_transcription(self, raw_text: str, api_choice: str = "deepseek") -> str:
        """
        LLMを使用して文字起こし精度を向上
        
        Args:
            raw_text: Whisperの生テキスト
            api_choice: 使用するAPI (deepseek, gemini, openai)
            
        Returns:
            改善されたテキスト
        """
        if api_choice not in self.available_apis:
            raise ValueError(f"API '{api_choice}' は利用できません。利用可能: {self.available_apis}")
        
        prompt = self._create_improvement_prompt(raw_text)
        
        try:
            if api_choice == "deepseek":
                return self._call_deepseek_api(prompt)
            elif api_choice == "openai":
                return self._call_openai_api(prompt)
            elif api_choice == "gemini":
                return self._call_gemini_api(prompt)
            else:
                raise ValueError(f"サポートされていないAPI: {api_choice}")
        except Exception as e:
            print(f"LLM処理でエラーが発生: {e}")
            print("元のテキストを返します")
            return raw_text
    
    def _create_improvement_prompt(self, raw_text: str) -> str:
        """文字起こし改善用プロンプトを作成"""
        return f"""以下は日本の会議音声をWhisperで文字起こしした結果です。
会議記録として適切になるよう、以下の点を修正してください：

1. 音声認識の誤認識を修正
2. 適切な句読点・改行を追加  
3. 話し言葉を自然な書き言葉に調整
4. 専門用語・固有名詞の正確性確保
5. タイムスタンプ形式 [HH:MM:SS - HH:MM:SS] は必ず保持してください

【修正対象テキスト】
{raw_text}

【修正後テキスト】"""
    
    def _call_deepseek_api(self, prompt: str) -> str:
        """DeepSeek APIを呼び出し"""
        headers = {
            "Authorization": f"Bearer {self.config.DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1
        }
        
        response = requests.post(
            self.config.DEEPSEEK_API_URL,
            headers=headers,
            json=data,
            timeout=60
        )
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    
    def _call_openai_api(self, prompt: str) -> str:
        """OpenAI APIを呼び出し"""
        client = openai.OpenAI(api_key=self.config.OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        
        return response.choices[0].message.content.strip()
    
    def _call_gemini_api(self, prompt: str) -> str:
        """Gemini APIを呼び出し"""
        # Gemini API実装（Google AI Studio API）
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={self.config.GEMINI_API_KEY}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.1
            }
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"].strip()
    
    def estimate_cost(self, text: str, api_choice: str) -> float:
        """
        処理コストを概算
        
        Args:
            text: 処理するテキスト
            api_choice: 使用するAPI
            
        Returns:
            推定コスト（USD）
        """
        # 簡易的なトークン数計算（日本語: 約2文字=1トークン）
        estimated_tokens = len(text) // 2
        
        # API別料金（1Mトークンあたり）
        rates = {
            "deepseek": 0.14,
            "gemini": 0.075, 
            "openai": 0.15
        }
        
        rate = rates.get(api_choice, 0.15)
        return (estimated_tokens / 1000000) * rate