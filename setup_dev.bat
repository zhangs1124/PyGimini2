@echo off
setlocal enabledelayedexpansion
title 專案開發環境初始化工具

echo ===================================================
echo        🚀 專案開發環境一鍵初始化 (Groq API)
echo ===================================================
echo.

set "KEY_FOUND="

:: 1. 檢查系統環境變數
echo [1/3] 正在檢查系統環境變數...
if not "%GROQ_API_KEY%"=="" (
    echo    v 找到系統變數 GROQ_API_KEY
    set "KEY_FOUND=%GROQ_API_KEY%"
) else (
    echo    x 系統變數中找不到金鑰
)

:: 2. 檢查 Git 全域設定 (如果您系統變數沒設，但 Git 有設)
if "!KEY_FOUND!"=="" (
    echo [2/3] 正在檢查 Git 全域設定...
    for /f "tokens=*" %%i in ('git config --global user.groq-api-key 2^>nul') do set "GIT_KEY=%%i"
    if not "!GIT_KEY!"=="" (
        echo    v 找到 Git 全域金鑰
        set "KEY_FOUND=!GIT_KEY!"
        
        echo    ! 正在將 Git 金鑰同步至系統環境變數以供 Python 使用...
        setx GROQ_API_KEY "!GIT_KEY!" >nul
    ) else (
        echo    x Git 全域設定中也找不到金鑰
    )
)

:: 3. 如果通通找不到，則提示輸入
if "!KEY_FOUND!"=="" (
    echo.
    echo ---------------------------------------------------
    echo [!] 偵測不到任何金鑰設定。
    set /p "USER_INPUT=請貼上您的 Groq API Key (gsk_...): "
    
    if "!USER_INPUT!"=="" (
        echo 錯誤：未輸入金鑰，初始化失敗。
        pause
        exit /b
    )
    
    set "KEY_FOUND=!USER_INPUT!"
    
    echo    ! 正在永久儲存金鑰至系統環境變數...
    setx GROQ_API_KEY "!USER_INPUT!" >nul
    
    echo    ! 正在永久儲存金鑰至 Git 全域設定...
    git config --global user.groq-api-key "!USER_INPUT!"
)

:: 4. 產生本機專案的 .env 檔案 (許多 Python 套件首選)
echo [3/3] 正在建立本機 .env 設定檔...
echo GROQ_API_KEY=!KEY_FOUND! > .env
echo    v 已建立 .env 檔案並自動加入金鑰

echo.
echo ===================================================
echo    🎉 初始化成功！
echo    1. 系統環境變數已就緒
echo    2. Git 全域設定已同步
echo    3. 本機 .env 檔案已產生
echo.
echo 提示：如果您是第一次設定環境變數，請重啟 VS Code。
echo ===================================================
pause
