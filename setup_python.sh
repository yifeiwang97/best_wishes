#!/bin/bash

# 语音克隆应用 - Python 环境自动配置脚本

set -e  # 遇到错误立即退出

echo "=================================="
echo "  语音克隆应用 - 环境配置脚本"
echo "=================================="
echo ""

# 项目目录
PROJECT_DIR="/Users/feifei/work/self-interest/bestwishes"
cd "$PROJECT_DIR"

# 查找 Python 3.10 或更高版本
echo "🔍 查找 Python 3.10+..."
PYTHON=""

# 可能的 Python 路径
PYTHON_PATHS=(
    "/usr/local/bin/python3.10"
    "/usr/local/bin/python3.11"
    "/usr/local/bin/python3.12"
    "/usr/local/opt/python@3.10/bin/python3.10"
    "/usr/local/opt/python@3.11/bin/python3.11"
    "/Library/Frameworks/Python.framework/Versions/3.10/bin/python3.10"
    "/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11"
    "/opt/homebrew/bin/python3.10"
    "/opt/homebrew/bin/python3.11"
)

for py in "${PYTHON_PATHS[@]}"; do
    if [ -f "$py" ]; then
        VERSION=$($py -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        MAJOR=$(echo $VERSION | cut -d. -f1)
        MINOR=$(echo $VERSION | cut -d. -f2)
        
        if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 9 ]; then
            PYTHON="$py"
            echo "✅ 找到 Python $VERSION: $py"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo ""
    echo "❌ 未找到 Python 3.9 或更高版本"
    echo ""
    echo "请按照以下步骤安装："
    echo ""
    echo "1️⃣  访问 Python 官网："
    echo "   https://www.python.org/downloads/macos/"
    echo ""
    echo "2️⃣  下载 Python 3.10.x"
    echo "   (点击 'Download macOS 64-bit universal2 installer')"
    echo ""
    echo "3️⃣  双击 .pkg 文件安装"
    echo ""
    echo "4️⃣  安装完成后重新运行此脚本"
    echo ""
    exit 1
fi

# 删除旧的虚拟环境
if [ -d "venv" ]; then
    echo ""
    echo "🧹 删除旧的虚拟环境..."
    rm -rf venv
fi

# 创建虚拟环境
echo ""
echo "📦 创建虚拟环境..."
$PYTHON -m venv venv

# 激活虚拟环境
echo "🔌 激活虚拟环境..."
source venv/bin/activate

# 验证 Python 版本
VENV_VERSION=$(python --version)
echo "✅ 虚拟环境 Python: $VENV_VERSION"

# 升级 pip
echo ""
echo "⬆️  升级 pip..."
python -m pip install --upgrade pip --quiet

# 检查是否需要安装 ffmpeg
echo ""
echo "🔍 检查 ffmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  未检测到 ffmpeg（音频处理需要）"
    echo "   建议安装: brew install ffmpeg"
    echo "   但会继续安装 Python 依赖..."
else
    echo "✅ ffmpeg 已安装"
fi

# 安装依赖
echo ""
echo "📥 安装项目依赖..."
echo "   这可能需要 5-10 分钟，请耐心等待..."
echo ""

cd backend

# 尝试使用国内镜像加速（如果连接 PyPI 慢的话）
echo "尝试使用清华镜像源..."
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple 2>/dev/null || {
    echo "清华镜像失败，使用官方源..."
    pip install -r requirements.txt
}

cd ..

# 运行环境检查
echo ""
echo "🧪 运行环境检查..."
python test_setup.py

echo ""
echo "=================================="
echo "  🎉 环境配置完成！"
echo "=================================="
echo ""
echo "🚀 启动应用："
echo ""
echo "   cd $PROJECT_DIR"
echo "   source venv/bin/activate"
echo "   cd backend"
echo "   python main.py"
echo ""
echo "或者直接运行："
echo ""
echo "   ./start.sh"
echo ""
echo "然后访问: http://localhost:8000"
echo ""
echo "=================================="
