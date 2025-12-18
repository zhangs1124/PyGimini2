@echo off
setlocal enabledelayedexpansion
title 專案開發環境全自動初始化工具

echo ===================================================
echo        🚀 專案開發環境全自動初始化 (AI + GitHub)
echo ===================================================
echo.

:: --- 1. 檢查與設定 GROQ_API_KEY ---
echo [1/2] 正在檢查 Groq API 金鑰...
set "GROQ_KEY="
if not "%GROQ_API_KEY%"=="" (
    echo    v 找到系統變數 GROQ_API_KEY
    set "GROQ_KEY=%GROQ_API_KEY%"
) else (
    for /f "tokens=*" %%i in ('git config --global user.groq-api-key 2^>nul') do set "GROQ_KEY=%%i"
    if not "!GROQ_KEY!"=="" (
        echo    v 找到 Git 全域金鑰，正在同步至系統變數...
        setx GROQ_API_KEY "!GROQ_KEY!" >nul
    ) else (
        echo    ! 警告：找不到 Groq 金鑰！請手動設定或聯繫管理員。
    )
)

:: --- 2. 檢查與設定 GITHUB_TOKEN ---
echo.
echo [2/2] 正在檢查 GitHub 認證 Token...
if not "%GITHUB_TOKEN%"=="" (
    echo    v 找到系統變數 GITHUB_TOKEN
    echo    ! 正在設定 Git 認證助手為 wincred...
    git config --global credential.helper wincred
) else (
    echo    x 系統中找不到 GITHUB_TOKEN！
    echo    提示：建議產生一個 Personal Access Token 並執行 [setx GITHUB_TOKEN "your_token"]
)

:: --- 3. 產生本地 .env 檔案 ---
echo.
echo ---------------------------------------------------
echo 正在建立/更新本機 .env 設定檔...

:: 建立檔案 (Overwrite)
echo # 專案環境設定 > .env
if not "!GROQ_KEY!"=="" (
    echo GROQ_API_KEY=!GROQ_KEY! >> .env
    echo    + 已寫入 GROQ_API_KEY
)
if not "%GITHUB_TOKEN%"=="" (
    echo GITHUB_TOKEN=%GITHUB_TOKEN% >> .env
    echo    + 已寫入 GITHUB_TOKEN
)

echo.
echo ===================================================
echo    🎉 初始化與同步完成！
echo    1. Groq 金鑰已就緒
echo    2. GitHub 認證已就緒 (wincred)
echo    3. 本機 .env 已完美對齊
echo.
echo 提示：若這是您第一次設定 Token，建議重新啟動您的 IDE。
echo ===================================================
pause
