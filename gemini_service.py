"""
此模組提供了與Google Gemini API交互的服務類
"""
import aiohttp
import json
from typing import Optional

class GeminiService:
    """
    GeminiService類用於與Google Gemini API進行通信
    
    屬性:
        _api_key (str): Google Gemini API金鑰
        _base_url (str): API基礎URL
    """
    
    def __init__(self, api_key: str):
        """
        初始化GeminiService實例
        
        參數:
            api_key (str): Google Gemini API金鑰
        """
        self._api_key = api_key
        self._base_url = "https://generativelanguage.googleapis.com/v1beta/"
        
    async def get_response(self, prompt: str) -> str:
        """
        向Gemini API發送請求並獲取回應
        
        參數:
            prompt (str): 要發送給API的提示文本
            
        返回:
            str: API的回應文本或錯誤信息
        """
        try:
            request_data = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ]
            }
            
            async with aiohttp.ClientSession() as session:
                url = f"{self._base_url}models/gemini-2.0-flash:generateContent?key={self._api_key}"
                async with session.post(url, json=request_data) as response:
                    response.raise_for_status()
                    result = await response.json()
                    
                    return (result.get("candidates", [{}])[0]
                           .get("content", {})
                           .get("parts", [{}])[0]
                           .get("text", "無回應"))
                           
        except Exception as ex:
            return f"錯誤：{str(ex)}" 