import os
import subprocess

def get_git_global(key):
    try:
        result = subprocess.run(
            ['git', 'config', '--global', key], 
            capture_output=True, 
            text=True
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except:
        return None

print("\n" + "="*50)
print(" 🛡️ 全系統安全設定測試 (OS + Git Global)")
print("="*50)

# 1. 檢查 Git 全域設定
print("[Git 全域層級]")
global_groq = get_git_global('user.groq-api-key')
if global_groq:
    print(f"  ✅ Git 全域 Groq Key: {global_groq[:10]}...")
else:
    print("  ❌ Git 全域設定中找不到 groq-api-key")

helper = get_git_global('credential.helper')
print(f"  ℹ️ Git 認證助手狀態: {helper if helper else '未設定'}")

# 2. 檢查作業系統環境變數 (這是我們剛剛重點設定的地方)
print("\n[作業系統 OS 層級]")

env_groq = os.environ.get('GROQ_API_KEY')
if env_groq:
    print(f"  ✅ OS 環境變數 (Groq): {env_groq[:10]}...")
else:
    print("  ❌ OS 環境變數中找不到 GROQ_API_KEY")

env_github = os.environ.get('GITHUB_TOKEN')
if env_github:
    print(f"  ✅ OS 環境變數 (GitHub): {env_github[:10]}...")
else:
    print("  ❌ OS 環境變數中找不到 GITHUB_TOKEN")

print("\n" + "="*50)
print("結論：只要上面的 ✅ 越多，您的環境就越「自動化」且越安全！")
print("="*50)
