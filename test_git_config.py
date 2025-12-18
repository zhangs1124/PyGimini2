import subprocess

def get_git_key():
    try:
        # 執行 git config 指令來獲取我們存入的值
        result = subprocess.run(
            ['git', 'config', '--get', 'groq.api-key'], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

key = get_git_key()

print("\n--- Git Config 儲存測試 ---")
if key:
    print(f"解析成功！從 Git 設定中抓取到 Key: {key[:10]}...")
    print("這表示您的金鑰現在隱藏在 .git 資料夾中，非常安全且不佔用環境變數。")
else:
    print("失敗：Git 設定中找不到該金鑰。")
