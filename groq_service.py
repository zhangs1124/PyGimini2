"""
此模組提供了與 Groq API 交互的服務類
"""
import aiohttp
import json
from typing import Optional

class GroqService:
    """
    GroqService 類用於與 Groq API 進行通信 (OpenAI 相容格式)
    
    屬性:
        _api_key (str): Groq API 金鑰
        _base_url (str): API 基礎 URL
        _model (str): 使用的模型名稱
    """
    
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        """
        初始化 GroqService 實例
        
        參數:
            api_key (str): Groq API 金鑰
            model (str): 模型名稱
        """
        self._api_key = api_key
        self._base_url = "https://api.groq.com/openai/v1/chat/completions"
        self._model = model
        
    async def get_response(self, prompt: str) -> str:
        """
        向 Groq API 發送請求並獲取回應
        
        參數:
            prompt (str): 要發送給 API 的提示文本
            
        返回:
            str: API 的回應文本或錯誤信息
        """
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json"
        }
        
        request_data = {
            "model": self._model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self._base_url, headers=headers, json=request_data) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        return f"錯誤：HTTP {response.status} - {error_text}"
                    
                    result = await response.json()
                    return result["choices"][0]["message"]["content"]
                           
        except Exception as ex:
            return f"發生異常：{str(ex)}" 
