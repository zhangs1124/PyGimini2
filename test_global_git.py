import subprocess

def get_global_key():
    try:
        # 使用 --global 參數讀取
        result = subprocess.run(
            ['git', 'config', '--global', 'user.groq-api-key'], 
            capture_output=True, 
            text=True
        )
        return result.stdout.strip()
    except:
        return None

key = get_global_key()

print("\n--- Git 全域設定測試 ---")
if key:
    print(f"成功讀取全域設定！Key: {key[:10]}...")
    print("成果：即便您明天開一個全新的專案，只要執行上述 Python 代碼，就能抓到同一個 Key！")
else:
    print("失敗：找不到全域設定。")
