import os

# 從作業系統讀取環境變數
api_key = os.environ.get('GROQ_API_KEY')

print("\n--- 環境變數測試 ---")
if api_key:
    # 遮罩顯示，只顯示前後幾個字
    masked_key = f"{api_key[:10]}...{api_key[-5:]}"
    print(f"成功連線保險箱！偵測到 Key: {masked_key}")
    print("狀態：已就緒 (不需要讀取任何檔案)")
else:
    print("失敗：找不到 GROQ_API_KEY。")
    print("提示：如果您是手動在視窗設定的，可能需要重啟 IDE/終端機。")
