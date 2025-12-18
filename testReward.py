import asyncio
from edge_playwright_controller import EdgePlaywrightController

async def test_rewards():
    """測試Bing Rewards積分檢查功能"""
    try:
        # 初始化控制器
        controller = EdgePlaywrightController()
        
        # 獲取設定檔列表
        profiles = controller.get_profiles()
        if not profiles:
            print("找不到任何Edge瀏覽器設定檔！")
            return
            
        # 使用第一個設定檔
        profile_index = 0
        print(f"\n使用設定檔 {profile_index}: {profiles[profile_index]['display_name']}")
        
        # 啟動瀏覽器
        await controller.start(profile_index)
        
        # 檢查積分
        current_points, max_points = await controller.check_bing_rewards_points()
        print(f"\n檢查結果：")
        print(f"當前積分：{current_points}")
        print(f"最大積分：{max_points}")
        
        # 保持瀏覽器開啟
        print("\n測試完成！瀏覽器保持開啟中...")
        print("按Ctrl+C結束程式")
        
        # 等待用戶手動結束程式
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        print("\n程式已終止")
    except Exception as e:
        print(f"\n發生錯誤：{str(e)}")
    
if __name__ == "__main__":
    asyncio.run(test_rewards())