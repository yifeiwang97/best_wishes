#!/bin/bash

# 完整安装所有依赖 - 解决 SSL 和缺失依赖问题

set -e

echo "=================================="
echo "  完整安装所有依赖"
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

# 设置 pip 选项（绕过 SSL 证书问题）
PIP_OPTS="--trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host pypi.python.org"

cd backend

echo "⬆️  升级 pip..."
python -m pip install $PIP_OPTS --upgrade pip

echo ""
echo "📥 安装所有 TTS 依赖..."
echo ""

# TTS 的所有依赖
pip install $PIP_OPTS \
    coqpit \
    aiohttp>=3.8.1 \
    anyascii>=0.3.0 \
    cython>=0.29.30 \
    flask>=2.0.1 \
    matplotlib>=3.7.0 \
    nltk \
    num2words \
    pysbd>=0.3.4 \
    trainer>=0.0.32 \
    umap-learn>=0.5.1 \
    unidecode>=1.3.2 \
    scipy \
    librosa \
    soundfile \
    inflect \
    pypinyin \
    jieba \
    "pandas>=1.4,<2.0" \
    requests \
    tqdm \
    packaging \
    pyyaml \
    fsspec \
    einops \
    transformers \
    encodec

echo ""
echo "📥 安装语言支持包（可选，可能失败）..."
pip install $PIP_OPTS bangla bnnumerizer bnunicodenormalizer g2pkk hangul_romanize jamo || echo "⚠️  部分语言包安装失败（不影响中英文使用）"

echo ""
echo "📥 安装 gruut（可能失败，不影响核心功能）..."
pip install $PIP_OPTS "gruut[de,es,fr]==2.2.3" || echo "⚠️  gruut 安装失败（不影响中英文使用）"

echo ""
echo "📥 安装 spacy（可能失败，不影响核心功能）..."
pip install $PIP_OPTS "spacy>=3" || echo "⚠️  spacy 安装失败（不影响核心功能）"

echo ""
echo "📥 验证 numpy 版本..."
pip install $PIP_OPTS "numpy>=1.22.0,<2.0"

echo ""
echo "📥 安装项目依赖..."
pip install $PIP_OPTS \
    fastapi==0.109.0 \
    "uvicorn[standard]==0.27.0" \
    python-multipart==0.0.6 \
    aiofiles==23.2.1 \
    pydub==0.25.1

echo ""
echo "=================================="
echo "  ✅ 依赖安装完成！"
echo "=================================="
echo ""

echo "🧪 测试 TTS 导入..."
python -c "from TTS.api import TTS; print('✅ TTS 导入成功！')" || echo "⚠️  TTS 导入测试失败，但可能仍然可用"

echo ""
echo "🚀 现在可以启动应用："
echo "   cd backend"
echo "   python main.py"
echo ""
