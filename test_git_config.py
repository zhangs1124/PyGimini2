import subprocess
import os

def get_git_config(scope, key):
    try:
        result = subprocess.run(
            ['git', 'config', scope, key], 
            capture_output=True, 
            text=True
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except:
        return None

print("\n" + "="*40)
print(" 🔍 本地專案 Git 設定測試")
print("="*40)

# 測試 Groq Key
groq_key = get_git_config('--local', 'groq.api-key')
if groq_key:
    print(f"✅ 找到本地 Groq Key: {groq_key[:10]}...")
else:
    print("❌ 本地 .git/config 中找不到 groq.api-key")

# 測試 GitHub 遠端連線資訊
remote_url = get_git_config('--get', 'remote.origin.url')
if remote_url:
    print(f"✅ 找到遠端倉庫網址: {remote_url}")
else:
    print("❌ 找不到遠端倉庫連接資訊")

print("-" * 40)
print("提示：本地設定只對「這一個資料夾」有效。")
print("="*40)
