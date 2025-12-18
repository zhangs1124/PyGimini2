"""
此模組展示如何使用GeminiService生成問句並使用EdgePlaywrightController進行自動化搜尋
"""
import asyncio
import random
from edge_playwright_controller import EdgePlaywrightController
from gemini_service import GeminiService
from question_generator import QuestionGenerator
import time
import sys
import re

async def async_main():
    """
    主程序入口點
    """
    try:
        # 獲取命令列參數
        profile_index = 0  # 預設使用第一個設定檔
        if len(sys.argv) > 1:
            try:
                profile_index = int(sys.argv[1])
            except ValueError:
                print("錯誤：請輸入有效的設定檔編號！")
                return
        
        # 初始化Edge控制器
        controller = EdgePlaywrightController()
        
        # 獲取設定檔列表
        profiles = controller.get_profiles()
        if not profiles:
            print("找不到任何Edge瀏覽器設定檔！")
            return
            
        print(f"\n可用的設定檔：")
        for i, profile in enumerate(profiles):
            print(f"{i}. {profile['display_name']}")
        
        # 驗證設定檔索引是否有效
        if profile_index < 0 or profile_index >= len(profiles):
            print(f"錯誤：設定檔編號 {profile_index} 無效！可用的設定檔編號範圍是 0-{len(profiles)-1}")
            return
            
        print(f"\n使用設定檔 {profile_index}: {profiles[profile_index]['display_name']}")
        
        # 使用選擇的設定檔啟動瀏覽器
        try:
            await controller.start(profile_index)
        except Exception as e:
            print(f"啟動瀏覽器時發生錯誤：{str(e)}")
            return

        # 初始化服務
        api_key = "AIzaSyD0-iYabnvEZekAS3F_yj9-8KRClzhMcak"
        gemini_service = GeminiService(api_key)
        question_generator = QuestionGenerator()
        
        # 生成問題並獲取回答
        print("正在生成問題...")
        question = question_generator.generate_question()
        ans_model = """請給我10個簡單的搜尋問題，格式如下：
1. 第一個問題
2. 第二個問題
3. 第三個問題
...以此類推到第10個問題。
請直接列出問題，不要有其他說明文字。每個問題都要以數字加點開頭。"""
        question = question + ans_model
        
        print(f"生成的問題: {question}")
        print("\n正在獲取回答...\n")
        
        # 使用await直接獲取Gemini回答
        response = await gemini_service.get_response(question)
        print(f"Gemini的回答:\n{response}")
        
        # 將回答分割成問句列表
        questions = []
        for line in response.split('\n'):
            line = line.strip()
            if not line:  # 跳過空行
                continue
            # 使用更靈活的正則表達式來匹配問題
            match = re.match(r'^\s*(\d+)[\.\、\:]?\s*(.+)$', line)
            if match:
                question_number = int(match.group(1))
                question_text = match.group(2).strip()
                if 1 <= question_number <= 10 and question_text:
                    questions.append(question_text)
        
        # 如果沒有獲取到問句，直接結束程式
        if not questions:
            print("無法從回答中提取問句，程式結束。")
            await controller.close()
            sys.exit(1)
        
        # 設定要選擇的問句數量
        max_questions_to_select = 4  # 可以根據需要調整這個數量
        
        # 選擇要搜尋的問句（最多由變數控制的數量）
        selected_questions = questions[:max_questions_to_select] if len(questions) <= max_questions_to_select else random.sample(questions, max_questions_to_select)
            
        print("\n選擇的問句：")
        for i, q in enumerate(selected_questions, 1):
            print(f"{i}. {q}")
            
        # 依次搜尋選擇的問句
        for i, query in enumerate(selected_questions, 1):
            print(f"\n正在執行第 {i} 個搜尋查詢：{query}")
            try:
                await controller.search_query(query)
                
                if i < len(selected_questions):
                    # 較長的等待時間，模擬人工閱讀和思考
                    wait_time = random.uniform(10, 15)
                    print(f"\n停留 {wait_time:.1f} 秒閱讀結果...")
                    await asyncio.sleep(wait_time)  # 使用 asyncio.sleep 替代 time.sleep
            except Exception as e:
                print(f"搜尋時發生錯誤：{str(e)}")
                break
        
        print("\n搜尋完成！瀏覽器保持開啟中...")
        print("您可以：")
        print("1. 繼續瀏覽搜尋結果")
        print("2. 手動進行更多搜尋")
        print("3. 關閉瀏覽器結束程式")
            
    except Exception as ex:
        print(f"發生錯誤：{str(ex)}")
        sys.exit(1)

def main():
    """
    程式入口點
    """
    asyncio.run(async_main())

if __name__ == "__main__":
    main() 