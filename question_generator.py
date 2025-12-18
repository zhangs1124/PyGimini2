"""
此模組提供了問題生成器的實現
"""
import random
from typing import Dict, List

class QuestionGenerator:
    """
    QuestionGenerator類用於生成結構化的問題
    
    屬性:
        _parameters (Dict[str, List[str]]): 問題生成所需的參數字典
        _random (random.Random): 隨機數生成器
    """
    
    def __init__(self):
        """
        初始化QuestionGenerator實例
        """
        self._random = random.Random()
        self._parameters: Dict[str, List[str]] = {
            "領域": ["教育", "醫療", "金融", "科技", "環保", "人工智能", "娛樂", "運動", "藝術", "旅遊", "飲食", "時尚"],
            "結構": ["開放式", "邏輯樹狀", "流程圖解", "模組化", "互動式", "分散式", "階層式", "網狀", "循環式", "自適應"],
            "複雜度": ["基礎概念", "進階應用", "策略分析", "創新突破", "跨域整合", "前瞻研究", "實驗性質", "理論驗證", "市場驗證", "用戶體驗"],
            "教育階段": ["小學", "中學", "大學", "研究所", "職業培訓", "終身學習", "幼兒教育", "成人教育", "專業認證", "技職教育"],
            "商業類型": ["零售業", "製造業", "服務業", "科技業", "文創產業", "新創企業", "電商", "社群平台", "共享經濟", "訂閱服務"],
            "技術方法": ["深度學習", "機器學習", "自然語言處理", "電腦視覺", "強化學習", "聯邦學習", "區塊鏈", "物聯網", "擴增實境", "虛擬實境"],
            "實現方式": ["標準化流程", "彈性調整方案", "客製化解決方案", "智能自適應", "混合式架構", "微服務架構", "雲端服務", "邊緣運算", "分散式系統", "容器化部署"],
            "應用場景": ["遠距教學", "智慧醫療", "金融科技", "智慧城市", "永續發展", "元宇宙", "智慧家庭", "智慧交通", "智慧零售", "智慧工廠"],
            "評估指標": ["效率提升", "成本降低", "用戶體驗", "創新程度", "市場接受度", "社會影響力", "環境永續", "技術成熟度", "商業可行性", "安全性"],
            "目標族群": ["學生", "專業人士", "一般大眾", "銀髮族", "兒童", "青少年", "創業者", "研究人員", "教育工作者", "醫療人員"],
            "發展趨勢": ["數位轉型", "永續環保", "遠距工作", "個人化服務", "智慧化", "自動化", "去中心化", "跨域整合", "生態系統", "循環經濟"],
            "關注重點": ["使用者體驗", "資訊安全", "隱私保護", "成本效益", "市場需求", "技術創新", "社會責任", "法規遵循", "品質管理", "風險控制"]
        }
        
    def _get_random_value(self, parameter_key: str) -> str:
        """
        從指定參數中隨機獲取一個值
        
        參數:
            parameter_key (str): 參數鍵名
            
        返回:
            str: 隨機選擇的值
        """
        values = self._parameters[parameter_key]
        return self._random.choice(values)
        
    def generate_question(self) -> str:
        """
        生成結構化問題
        
        返回:
            str: 生成的問題
        """
        selected_domain = self._get_random_value("領域")
        question_template = ""
        
        if selected_domain == "教育":
            question_template = (
                f"在{self._get_random_value('應用場景')}的背景下，"
                f"如何在{self._get_random_value('教育階段')}階段，"
                f"運用{self._get_random_value('技術方法')}來實現{self._get_random_value('結構')}的"
                f"學習系統，並達到{self._get_random_value('複雜度')}的教學目標，"
                f"以提升{self._get_random_value('評估指標')}？"
            )
        elif selected_domain == "醫療":
            question_template = (
                f"在{self._get_random_value('應用場景')}的情境中，"
                f"如何結合{self._get_random_value('技術方法')}，"
                f"建立{self._get_random_value('結構')}的診斷支援系統，"
                f"以實現{self._get_random_value('複雜度')}層級的醫療決策輔助，"
                f"並確保{self._get_random_value('評估指標')}？"
            )
        elif selected_domain == "金融":
            question_template = (
                f"針對{self._get_random_value('商業類型')}在{self._get_random_value('應用場景')}中的應用，"
                f"如何運用{self._get_random_value('技術方法')}建立{self._get_random_value('實現方式')}，"
                f"以達成{self._get_random_value('複雜度')}的金融分析，"
                f"並優化{self._get_random_value('評估指標')}？"
            )
        elif selected_domain == "科技":
            question_template = (
                f"在{self._get_random_value('應用場景')}領域中，"
                f"如何將{self._get_random_value('技術方法')}與{self._get_random_value('實現方式')}結合，"
                f"建立{self._get_random_value('結構')}的創新系統，"
                f"實現{self._get_random_value('複雜度')}水平的技術突破？"
            )
        elif selected_domain == "環保":
            question_template = (
                f"為了實現{self._get_random_value('應用場景')}的永續發展，"
                f"如何運用{self._get_random_value('技術方法')}開發{self._get_random_value('結構')}的環保解決方案，"
                f"達到{self._get_random_value('複雜度')}的環境保護目標？"
            )
        elif selected_domain == "人工智能":
            question_template = (
                f"在{self._get_random_value('商業類型')}的{self._get_random_value('應用場景')}中，"
                f"如何整合{self._get_random_value('技術方法')}和{self._get_random_value('實現方式')}，"
                f"建立{self._get_random_value('結構')}的AI系統，"
                f"實現{self._get_random_value('複雜度')}的智能應用？"
            )
            
        return question_template 