@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ================================
echo    语音克隆应用 - 启动脚本
echo ================================
echo.

REM 检查 Docker 是否安装
where docker >nul 2>nul
if %errorlevel% equ 0 (
    where docker-compose >nul 2>nul
    if %errorlevel% equ 0 (
        echo ✓ 检测到 Docker，使用 Docker 部署...
        echo.
        
        REM 检查是否首次运行
        if not exist "models\" (
            echo ⚠️  首次运行提示：
            echo    首次启动需要下载约 1.8GB 的模型文件
            echo    请确保网络连接正常，并耐心等待...
            echo.
            pause
        )
        
        echo 🚀 正在启动服务...
        docker-compose up -d
        
        echo.
        echo ✅ 服务启动成功！
        echo.
        echo 📝 访问方式：
        echo    Web 界面: http://localhost:8000
        echo    API 文档: http://localhost:8000/docs
        echo.
        echo 📊 查看日志: docker-compose logs -f
        echo 🛑 停止服务: docker-compose down
        echo.
        pause
        exit /b 0
    )
)

REM 检查 Python 是否安装
where python >nul 2>nul
if %errorlevel% equ 0 (
    echo ⚠️  未检测到 Docker，使用本地 Python 部署...
    echo.
    
    REM 检查虚拟环境
    if not exist "venv\" (
        echo 📦 创建虚拟环境...
        python -m venv venv
    )
    
    echo 🔧 激活虚拟环境...
    call venv\Scripts\activate.bat
    
    REM 检查依赖
    if not exist "venv\.installed" (
        echo 📥 安装依赖（首次运行）...
        cd backend
        pip install -r requirements.txt
        cd ..
        echo. > venv\.installed
    )
    
    echo 🚀 启动服务...
    cd backend
    start /b python main.py
    cd ..
    
    echo.
    echo ✅ 服务启动成功！
    echo.
    echo 📝 访问方式：
    echo    Web 界面: http://localhost:8000
    echo    API 文档: http://localhost:8000/docs
    echo.
    echo 按任意键停止服务...
    pause >nul
    
    REM 停止服务
    taskkill /f /im python.exe /fi "WINDOWTITLE eq *uvicorn*" >nul 2>nul
    
    exit /b 0
)

echo ❌ 错误：未检测到 Docker 或 Python
echo.
echo 请先安装以下软件之一：
echo   • Docker ^& Docker Compose (推荐)
echo   • Python 3.10+
echo.
pause
exit /b 1
