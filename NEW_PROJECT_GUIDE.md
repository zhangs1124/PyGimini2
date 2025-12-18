# 🚀 新專案啟動標準流程 (SOP)

當您想要開啟一個全新的 AI 專案時，依照以下步驟可以確保環境安全且快速就緒：

### 1. 建立並進入新目錄
在終端機或檔案總管建立新資料夾：
```powershell
mkdir MyNewProject
cd MyNewProject
```

### 2. 初始化 Git (關鍵第一步)
為了讓後續設定生效，請先初始化 Git：
```powershell
git init
```

### 3. 加入核心安全設定
從舊專案 (PyGimini2) 複製以下兩個檔案到新專案：
*   `.gitignore` (確保 API Key 不會外流)
*   `setup_dev.bat` (萬用環境初始化工具)

### 4. 執行環境初始化
雙擊執行 `setup_dev.bat`。
*   **它會自動做什麼？** 
    1. 從您的系統或 Git 全域設定中抓取 `GROQ_API_KEY`。
    2. 在當前目錄產生 `.env` 檔案。
    3. 如果是新電腦，它會引導您輸入一次並收藏起來。

### 5. 開始開發
現在您可以開始寫 `main.py` 或 `index.html` 了。
*   **Python 讀取方式**：使用 `os.environ.get('GROQ_API_KEY')`。
*   **網頁讀取方式**：手動輸入或使用您寫好的 API 中轉。

### 6. 上傳至 GitHub
當程式寫到一個階段後：
1.  在 GitHub 上建立一個新的 Repository。
2.  執行連線指令：
    ```powershell
    git add .
    git commit -m "Initial commit"
    git branch -M main
    git remote add origin https://github.com/您的帳號/新專案名.git
    git push -u origin main
    ```

---
**💡 溫馨提醒：** 只要有 `.gitignore` 在，您就永遠不需要擔心 `.env` 或 `readme.md` 裡的敏感資訊被推送到網路上。
