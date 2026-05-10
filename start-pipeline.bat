@echo off
chcp 65001 >nul

cd /d %~dp0
echo ============================================
echo   SEO Pipeline 批量生产
echo ============================================
echo.
echo 用法:
echo   start-pipeline.bat run      批量处理所有待处理关键词
echo   start-pipeline.bat status   查看关键词进度
echo   start-pipeline.bat dry-run  验证配置
echo.
echo.

if "%1"=="" (
    python run.py status
) else (
    python run.py %*
)

pause
