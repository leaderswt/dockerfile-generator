@echo off
chcp 65001 >nul
echo.
echo ============================================================
echo           🐳 Dockerfile生成器启动脚本
echo ============================================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未检测到Python，请先安装Python 3.8+
    echo    下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

:: 检查依赖是否安装
echo 📦 检查依赖...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo 📥 正在安装依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
)

echo ✅ 依赖检查完成
echo.
echo 🚀 正在启动Dockerfile生成器...
echo.
echo 📍 访问地址: http://127.0.0.1:5000
echo 🌐 网络访问: http://192.168.0.7:5000
echo.
echo 📖 按 Ctrl+C 停止服务
echo ============================================================
echo.

python app.py

pause
