#!/bin/bash

# 语音克隆应用快速启动脚本

echo "================================"
echo "   语音克隆应用 - 启动脚本"
echo "================================"
echo ""

# 检查 Docker 是否安装
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo "✓ 检测到 Docker，使用 Docker 部署..."
    echo ""
    
    # 检查是否首次运行
    if [ ! -d "./models" ]; then
        echo "⚠️  首次运行提示："
        echo "   首次启动需要下载约 1.8GB 的模型文件"
        echo "   请确保网络连接正常，并耐心等待..."
        echo ""
        read -p "按 Enter 继续..." 
    fi
    
    echo "🚀 正在启动服务..."
    docker-compose up -d
    
    echo ""
    echo "✅ 服务启动成功！"
    echo ""
    echo "📝 访问方式："
    echo "   Web 界面: http://localhost:8000"
    echo "   API 文档: http://localhost:8000/docs"
    echo ""
    echo "📊 查看日志: docker-compose logs -f"
    echo "🛑 停止服务: docker-compose down"
    echo ""
    
elif command -v python3 &> /dev/null; then
    echo "⚠️  未检测到 Docker，使用本地 Python 部署..."
    echo ""
    
    # 检查虚拟环境
    if [ ! -d "venv" ]; then
        echo "📦 创建虚拟环境..."
        python3 -m venv venv
    fi
    
    echo "🔧 激活虚拟环境..."
    source venv/bin/activate
    
    # 检查依赖
    if [ ! -f "venv/.installed" ]; then
        echo "📥 安装依赖（首次运行）..."
        cd backend
        pip install -r requirements.txt
        cd ..
        touch venv/.installed
    fi
    
    echo "🚀 启动服务..."
    cd backend
    python main.py &
    SERVER_PID=$!
    cd ..
    
    echo ""
    echo "✅ 服务启动成功！"
    echo ""
    echo "📝 访问方式："
    echo "   Web 界面: http://localhost:8000"
    echo "   API 文档: http://localhost:8000/docs"
    echo ""
    echo "🛑 停止服务: kill $SERVER_PID"
    echo ""
    echo "按 Ctrl+C 停止服务"
    
    # 等待用户中断
    wait $SERVER_PID
    
else
    echo "❌ 错误：未检测到 Docker 或 Python3"
    echo ""
    echo "请先安装以下软件之一："
    echo "  • Docker & Docker Compose (推荐)"
    echo "  • Python 3.10+"
    echo ""
    exit 1
fi
