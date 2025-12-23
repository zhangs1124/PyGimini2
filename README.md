# 🤖 PyGimini2 - 高效能雙引擎 AI 助理

PyGimini2 是一個整合了 **Groq** 與 **Google Gemini** 雙重 AI 引擎的高效能開發框架。本專案致力於展示如何安全、快速地建構次世代 AI 應用，並提供完整的網頁端測試工具。

## ✨ 核心特色

*   **⚡ 雙引擎架構**：
    *   **Groq**：採用 LPU 推論技術，提供極致的秒回體驗 (Llama 3, Mixtral)。
    *   **Gemini**：整合 Google 最新 Gemini 3 / 2.5 系列模型，具備強大的長文本與推理能力。
*   **🛡️ 企業級安全配置**：
    *   採用「環境變數優先 (Environment-First)」策略。
    *   支援 Windows 系統級別金鑰存儲。
    *   Git 全域設定同步支援。
    *   自動化 `.env` 管理，確保 API Key 永不外洩。
*   **🛠️ 完整的測試工具**：
    *   提供獨立的 HTML5 網頁介面，支援 `localStorage` 記憶與模型切換。
    *   此專案包含全自動環境初始化腳本。

## 🚀 快速開始 (Quick Start)

### 1. 環境初始化 (只需執行一次)
本專案附帶了強大的自動化腳本，能幫您一鍵設定好所有金鑰與權限。

1.  進入專案目錄。
2.  雙擊執行 **`setup_dev.bat`**。
3.  腳本會自動檢查您的系統環境變數或 Git 設定：
    *   若已設定：自動同步至本機 `.env`。
    *   若未設定：引導您輸入 Groq / Gemini 金鑰，並永久存入系統保險箱。

### 2. 啟動網頁測試工具
本專案無需安裝複雜的 Python 依賴即可測試前端：

*   **Groq 測試**：開啟 `web/groq_sample1.html`
*   **Gemini 測試**：開啟 `web/gemini_sample1.html`

(建議使用 Edge 或 Chrome 瀏覽器開啟)

## 📂 專案結構

*   `setup_dev.bat` - **[核心]** 全自動環境初始化腳本。
*   `NEW_PROJECT_GUIDE.md` - 新專案開發標準流程 (SOP)。
*   `web/` - 網頁端應用程式。
    *   `groq_sample1.html` - Groq 專用測試儀表板。
    *   `gemini_sample1.html` - Gemini 專用測試儀表板。
*   `test_global_git.py` - 用於驗證全系統安全設定的測試腳本。

## 🔒 機密資訊管理 (Security)

本專案嚴格遵守 **Secrets Management** 最佳實踐：
1.  **不**將 .env 或含有 key 的檔案上傳至 GitHub。
2.  使用 `.gitignore` 排除敏感檔案。
3.  推薦使用 OS 環境變數 (`GROQ_API_KEY`, `GEMINI_API_KEY`) 作為單一真理來源 (SSOT)。

---
**Happy Coding!** 🚀
