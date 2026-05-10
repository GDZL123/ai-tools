@echo off
chcp 65001 >nul
set PATH=%PATH%;%LOCALAPPDATA%\Microsoft\WinGet\Packages\Hugo.Hugo.Extended_Microsoft.Winget.Source_8wekyb3d8bbwe

cd /d %~dp0site
echo ============================================
echo   Hugo 开发服务器启动中...
echo   浏览器打开: http://localhost:1313/
echo   按 Ctrl+C 停止
echo ============================================
echo.

hugo server --buildDrafts --noHTTPCache

pause
