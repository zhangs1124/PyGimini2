"""
此模組提供了使用playwright控制Microsoft Edge瀏覽器的功能
"""
import os
import json
import time
import random
import subprocess
import psutil
import asyncio
from typing import Dict, List, Optional, Any
from playwright.async_api import async_playwright, Browser, Page

class EdgePlaywrightController:
    """
    使用playwright控制Edge瀏覽器的類
    
    屬性:
        _browser: Edge瀏覽器實例
        _page: 當前頁面
        _debug_port: 調試端口
        _playwright: Playwright實例
    """
    
    def __init__(self, debug_port: int = 9222):
        """
        初始化控制器
        
        參數:
            debug_port (int): 調試端口號
        """
        self._browser = None
        self._page = None
        self._debug_port = debug_port
        self._playwright = None
        
    def _kill_edge_processes(self) -> None:
        """
        關閉所有Edge瀏覽器進程
        """
        print("\n正在關閉現有的Edge瀏覽器進程...")
        
        try:
            subprocess.run(['taskkill', '/F', '/IM', 'msedge.exe'], capture_output=True)
            subprocess.run(['taskkill', '/F', '/IM', 'msedgedriver.exe'], capture_output=True)
            print("已強制關閉Edge瀏覽器進程")
        except Exception as e:
            print(f"關閉進程時發生錯誤：{str(e)}")
        
        time.sleep(2)
        
        # 再次確認是否還有Edge進程
        edge_still_running = False
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] and proc.info['name'].lower() in ['msedge.exe', 'msedgedriver.exe']:
                    edge_still_running = True
                    proc.kill()
            except:
                pass
        
        if edge_still_running:
            print("警告：某些Edge進程可能仍在運行")
        else:
            print("所有Edge進程已完全關閉")
        
        time.sleep(2)
    
    def get_profiles(self) -> List[Dict[str, str]]:
        """
        獲取所有Edge瀏覽器設定檔
        
        返回:
            List[Dict[str, str]]: 設定檔列表
        """
        profiles = []
        user_data_dir = os.path.join(os.environ.get('LOCALAPPDATA', ''), 
                                    'Microsoft', 'Edge', 'User Data')
        
        try:
            # 讀取Local State文件獲取設定檔信息
            local_state_path = os.path.join(user_data_dir, "Local State")
            if os.path.exists(local_state_path):
                with open(local_state_path, 'r', encoding='utf-8') as f:
                    local_state = json.load(f)
                    if "profile" in local_state and "info_cache" in local_state["profile"]:
                        for profile_name, profile_info in local_state["profile"]["info_cache"].items():
                            profiles.append({
                                "name": profile_name,
                                "display_name": profile_info.get("name", profile_name)
                            })
            
            # 如果沒有找到設定檔，返回Default設定檔
            if not profiles:
                profiles.append({
                    "name": "Default",
                    "display_name": "Default"
                })
                
        except Exception as e:
            print(f"讀取設定檔信息失敗：{str(e)}")
            profiles.append({
                "name": "Default",
                "display_name": "Default"
            })
            
        return profiles
    
    def _is_port_in_use(self, port: int) -> bool:
        """
        檢查端口是否被使用
        
        參數:
            port (int): 要檢查的端口號
            
        返回:
            bool: 端口是否被使用
        """
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0
            
    async def start(self, profile_index: Optional[int] = None) -> None:
        """
        啟動Edge瀏覽器
        
        參數:
            profile_index (int, optional): 設定檔索引，如果為None則使用Default設定檔
        """
        try:
            # 關閉現有的Edge進程
            self._kill_edge_processes()
            
            # 獲取Edge路徑
            edge_paths = [
                r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
            ]
            edge_path = next((path for path in edge_paths if os.path.exists(path)), None)
            if not edge_path:
                raise Exception("找不到Edge瀏覽器！")
                
            # 獲取設定檔
            profiles = self.get_profiles()
            if profile_index is not None and 0 <= profile_index < len(profiles):
                profile = profiles[profile_index]["name"]
                print(f"\n使用設定檔：{profiles[profile_index]['display_name']}")
            else:
                profile = "Default"
                print("\n使用預設設定檔")
                
            # 設置用戶數據目錄
            user_data_dir = os.path.join(os.environ.get('LOCALAPPDATA', ''), 
                                       'Microsoft', 'Edge', 'User Data')
                                       
            # 啟動Edge瀏覽器
            cmd = f'"{edge_path}" --remote-debugging-port={self._debug_port} --user-data-dir="{user_data_dir}" --profile-directory="{profile}"'
            print(f"\n啟動Edge瀏覽器：\n{cmd}")
            
            # 使用異步的方式啟動瀏覽器
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # 等待端口開啟
            for _ in range(30):
                if self._is_port_in_use(self._debug_port):
                    print("Edge瀏覽器已啟動並準備就緒")
                    break
                await asyncio.sleep(1)
            else:
                raise Exception("啟動Edge瀏覽器超時")
            
            # 等待一下確保瀏覽器完全準備好
            await asyncio.sleep(3)
            
            # 連接到瀏覽器
            self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.connect_over_cdp(
                f"http://localhost:{self._debug_port}",
                timeout=30000
            )
            
            # 等待確保上下文已經創建
            await asyncio.sleep(1)
            
            if not self._browser.contexts:
                context = await self._browser.new_context()
                self._page = await context.new_page()
            else:
                self._page = self._browser.contexts[0].pages[0] if self._browser.contexts[0].pages else await self._browser.contexts[0].new_page()
            
            print("已成功連接到Edge瀏覽器")
            
        except Exception as e:
            print(f"啟動Edge瀏覽器失敗：{str(e)}")
            if self._browser:
                await self._browser.close()
            if self._playwright:
                await self._playwright.stop()
            self._browser = None
            self._playwright = None
            self._page = None
            raise
            
    async def navigate(self, url: str, wait_load: bool = True) -> None:
        """
        導航到指定URL
        
        參數:
            url (str): 要訪問的URL
            wait_load (bool): 是否等待頁面加載完成
        """
        if not self._page:
            raise Exception("瀏覽器未啟動")
            
        try:
            print(f"\n正在訪問：{url}")
            if wait_load:
                await self._page.goto(url, wait_until="domcontentloaded", timeout=30000)
            else:
                await self._page.goto(url)
            print("頁面載入完成")
        except Exception as e:
            print(f"導航失敗：{str(e)}")
            raise
            
    async def close(self) -> None:
        """
        關閉瀏覽器
        """
        try:
            if self._browser:
                await self._browser.close()
                self._browser = None
            if self._playwright:
                await self._playwright.stop()
                self._playwright = None
            self._page = None
            self._kill_edge_processes()
            print("\nEdge瀏覽器已關閉")
        except Exception as e:
            print(f"關閉瀏覽器失敗：{str(e)}")
            
    def get_page(self) -> Optional[Page]:
        """
        獲取當前頁面對象
        
        返回:
            Optional[Page]: 當前頁面對象，如果瀏覽器未啟動則返回None
        """
        return self._page 
    
    async def type_like_human(self, selector: str, text: str) -> None:
        """
        模擬人工輸入文字
        
        參數:
            selector (str): 元素選擇器
            text (str): 要輸入的文字
        """
        if not self._page:
            raise Exception("瀏覽器未啟動")
            
        try:
            element = self._page.locator(selector)
            await element.click()
            
            for char in text:
                await element.type(char, delay=random.uniform(100, 300))
                time.sleep(random.uniform(0.1, 0.3))
                
        except Exception as e:
            print(f"輸入文字失敗：{str(e)}")
            raise
            
    async def search_query(self, query: str) -> None:
        """
        在Bing中搜尋查詢
        
        參數:
            query (str): 搜尋查詢
        """
        try:
            await self.navigate("https://www.bing.com")
            await self.type_like_human("#sb_form_q", query)
            await self._page.keyboard.press("Enter")
            await self._page.wait_for_load_state("domcontentloaded")
            
        except Exception as e:
            print(f"搜尋失敗：{str(e)}")
            raise
            
    async def check_bing_rewards_points(self) -> tuple[int, int]:
        """
        檢查Bing Rewards積分
        
        返回:
            tuple[int, int]: (當前積分, 最大積分)
        """
        if not self._page:
            raise Exception("瀏覽器未啟動")
            
        try:
            # 訪問Bing Rewards頁面
            print("\n正在檢查Bing Rewards積分...")
            await self.navigate("https://rewards.bing.com/pointsbreakdown")
            
            # 等待頁面加載
            await self._page.wait_for_load_state("networkidle")
            await self._page.wait_for_load_state("domcontentloaded")
            await asyncio.sleep(3)
            
            # 使用更精確的選擇器
            selector = "p.pointsDetail.c-subheading-3"
            element = await self._page.wait_for_selector(selector, timeout=5000)
            
            if element:
                # 獲取文本內容
                text = await element.text_content()
                print(f"找到積分元素：{text}")
                
                # 使用簡單的正則表達式提取數字
                import re
                numbers = re.findall(r'\d+', text)
                if len(numbers) >= 2:
                    current_points = int(numbers[0])
                    max_points = int(numbers[1])
                    print(f"當前PC搜索積分：{current_points}/{max_points}")
                    return current_points, max_points
            
            print("未找到積分元素，使用預設值：0/90")
            return 0, 90
            
        except Exception as e:
            print(f"檢查積分失敗：{str(e)}")
            return 0, 90