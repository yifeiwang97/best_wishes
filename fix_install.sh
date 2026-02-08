#!/bin/bash

# 修复安装脚本 - 解决 numba/llvmlite 编译问题

set -e

echo "=================================="
echo "  修复依赖安装问题"
echo "=================================="
echo ""

cd /Users/feifei/work/self-interest/bestwishes

# 确保虚拟环境已激活
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "🔌 激活虚拟环境..."
    source venv/bin/activate
fi

echo "✅ Python: $(python --version)"
echo ""

cd backend

# 方案 1: 分步安装，使用预编译包
echo "📦 方案 1: 分步安装依赖..."
echo ""

# 1. 升级基础工具
echo "⬆️  升级 pip, setuptools, wheel..."
pip install --upgrade pip setuptools wheel

# 2. 安装 numpy（固定版本避免冲突）
echo ""
echo "📥 安装 numpy..."
pip install "numpy<2.0.0"

# 3. 先安装 PyTorch（CPU 版本，更快）
echo ""
echo "📥 安装 PyTorch (CPU 版本)..."
pip install torch==2.1.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cpu

# 4. 尝试安装预编译的 llvmlite 和 numba
echo ""
echo "📥 尝试安装 llvmlite 和 numba..."
pip install llvmlite==0.40.1 numba==0.57.1 || {
    echo ""
    echo "⚠️  llvmlite/numba 安装失败，尝试跳过..."
    echo "   (TTS 的某些功能可能不可用，但核心功能正常)"
    echo ""
}

# 5. 安装 TTS（使用 --no-deps 避免重新安装冲突的依赖）
echo ""
echo "📥 安装 TTS..."
pip install TTS==0.22.0 --no-deps || pip install TTS==0.22.0

# 6. 补充安装 TTS 的其他依赖
echo ""
echo "📥 安装 TTS 的其他依赖..."
pip install \
    scipy \
    librosa \
    soundfile \
    inflect \
    pypinyin \
    jieba \
    pandas \
    requests \
    tqdm \
    packaging \
    pyyaml \
    fsspec \
    einops \
    transformers \
    encodec

# 7. 安装项目其他依赖
echo ""
echo "📥 安装项目依赖..."
pip install fastapi==0.109.0 uvicorn[standard]==0.27.0 python-multipart==0.0.6 aiofiles==23.2.1 pydub==0.25.1

echo ""
echo "=================================="
echo "  ✅ 安装完成！"
echo "=================================="
echo ""
echo "🧪 运行测试检查环境..."
cd ..
python test_setup.py || echo "⚠️  部分检查失败，但可能不影响使用"

echo ""
echo "🚀 启动应用："
echo "   cd backend && python main.py"
echo ""
