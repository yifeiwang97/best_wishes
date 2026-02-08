# 🔧 故障排除指南 - numba/llvmlite 编译失败

## 问题说明

遇到错误：
```
Error: failed-wheel-build-for-install
× Failed to build installable wheels for some pyproject.toml based projects
╰─> numba, llvmlite
```

这是因为 `numba` 和 `llvmlite` 需要编译，但在某些环境下编译失败。

---

## ✅ 解决方案（按推荐顺序）

### 方案 1：使用修复脚本（最简单，推荐）

我已经为您准备了自动修复脚本：

```bash
cd /Users/feifei/work/self-interest/bestwishes

# 确保虚拟环境已激活
source venv/bin/activate

# 运行修复脚本
./fix_install.sh
```

**这个脚本会**：
- ✅ 分步安装依赖，避免版本冲突
- ✅ 使用预编译的 wheel 包
- ✅ 如果 numba 失败，自动跳过（不影响核心功能）
- ✅ 安装所有必需的依赖

**预计耗时**：5-10 分钟

---

### 方案 2：手动分步安装

如果脚本失败，可以手动执行：

```bash
cd /Users/feifei/work/self-interest/bestwishes
source venv/bin/activate
cd backend

# 1. 升级工具
pip install --upgrade pip setuptools wheel

# 2. 安装 numpy
pip install "numpy<2.0.0"

# 3. 安装 PyTorch（CPU 版本）
pip install torch==2.1.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cpu

# 4. 尝试安装 llvmlite 和 numba（可能失败，没关系）
pip install llvmlite==0.40.1 numba==0.57.1 || echo "跳过 numba"

# 5. 安装 TTS（忽略依赖冲突）
pip install TTS==0.22.0 --no-deps

# 6. 安装 TTS 的其他依赖
pip install scipy librosa soundfile inflect pypinyin jieba pandas requests tqdm packaging pyyaml fsspec einops transformers encodec

# 7. 安装项目依赖
pip install fastapi uvicorn[standard] python-multipart aiofiles pydub
```

---

### 方案 3：跳过 numba（推荐如果编译一直失败）

`numba` 主要用于加速某些操作，但不是必需的。可以完全跳过：

```bash
cd /Users/feifei/work/self-interest/bestwishes
source venv/bin/activate
cd backend

# 直接安装，忽略 numba 错误
pip install --upgrade pip setuptools wheel
pip install "numpy<2.0.0"
pip install torch==2.1.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cpu
pip install TTS==0.22.0 --no-deps --no-build-isolation || pip install TTS --no-deps
pip install scipy librosa soundfile inflect pypinyin jieba pandas requests tqdm packaging pyyaml fsspec einops transformers encodec
pip install fastapi uvicorn[standard] python-multipart aiofiles pydub

# 测试
cd ..
python -c "from TTS.api import TTS; print('TTS 导入成功！')"
```

---

### 方案 4：使用更新的 Python 版本

如果使用的是 Python 3.10，尝试 Python 3.11（对 numba 支持更好）：

```bash
# 安装 Python 3.11
brew install python@3.11

# 重新创建虚拟环境
cd /Users/feifei/work/self-interest/bestwishes
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate

# 运行修复脚本
./fix_install.sh
```

---

## 🔍 深入排查

### 检查当前环境

```bash
# 检查 Python 版本
python --version

# 检查编译器
clang --version

# 检查 Xcode Command Line Tools
xcode-select -p

# 检查 pip 版本
pip --version
```

### 常见原因和解决方法

#### 原因 1：编译器版本不兼容

**症状**：编译时出现 C++ 错误

**解决**：
```bash
# 更新 Xcode Command Line Tools
sudo rm -rf /Library/Developer/CommandLineTools
xcode-select --install
```

#### 原因 2：Python 版本太旧或太新

**症状**：numba 不支持当前 Python 版本

**解决**：
- Python 3.10 或 3.11 是最稳定的
- 避免使用 Python 3.12+（numba 支持可能有问题）

#### 原因 3：架构不匹配（Apple Silicon）

**症状**：在 M1/M2 Mac 上编译失败

**解决**：
```bash
# 确保使用原生 ARM 版本
arch -arm64 pip install llvmlite numba

# 或者使用 Rosetta
arch -x86_64 pip install llvmlite numba
```

#### 原因 4：缓存问题

**症状**：反复编译失败

**解决**：
```bash
# 清理 pip 缓存
pip cache purge

# 清理构建目录
rm -rf build/ dist/ *.egg-info

# 重新安装
pip install --no-cache-dir llvmlite numba
```

---

## 📊 验证安装

运行以下命令检查安装是否成功：

```bash
cd /Users/feifei/work/self-interest/bestwishes
source venv/bin/activate

# 测试 1：检查 TTS 是否可以导入
python -c "from TTS.api import TTS; print('✅ TTS 导入成功')"

# 测试 2：检查所有依赖
python test_setup.py

# 测试 3：尝试加载模型（会下载模型）
python -c "
from TTS.api import TTS
print('正在测试 TTS 模型...')
tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2')
print('✅ 模型加载成功')
"
```

---

## 🎯 最终测试

安装完成后，启动应用测试：

```bash
cd /Users/feifei/work/self-interest/bestwishes
source venv/bin/activate
cd backend
python main.py
```

如果看到：
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

说明启动成功！访问 http://localhost:8000 测试。

---

## 💡 关于 numba 的说明

**numba 的作用**：
- 加速某些数值计算
- TTS 的部分功能使用它来提升速度

**没有 numba 的影响**：
- ✅ 核心语音合成功能**完全正常**
- ⚠️  某些操作可能稍慢（通常感觉不到）
- ✅ 不影响最终音频质量

**结论**：如果 numba 安装失败，**可以继续使用**，不必担心！

---

## 🆘 还是无法解决？

### 终极方案：使用 Docker

如果 Python 环境问题太复杂，强烈建议使用 Docker：

```bash
# 安装 Docker Desktop（如果还没有）
# https://www.docker.com/products/docker-desktop/

# 启动应用（无需担心 Python 依赖）
cd /Users/feifei/work/self-interest/bestwishes
docker-compose up -d

# 一切都配置好了！
```

Docker 方式的优势：
- ✅ 无需处理 Python 版本
- ✅ 无需编译任何东西
- ✅ 环境完全隔离
- ✅ 一键部署

---

## 📚 相关资源

- **numba 官方文档**：https://numba.pydata.org/
- **TTS 项目地址**：https://github.com/coqui-ai/TTS
- **PyTorch 安装指南**：https://pytorch.org/get-started/locally/

---

## 🔄 快速命令参考

```bash
# 方案 1：自动修复（推荐）
./fix_install.sh

# 方案 2：跳过 numba
pip install TTS --no-deps && pip install [其他依赖]

# 方案 3：使用 Docker
docker-compose up -d

# 验证安装
python test_setup.py

# 启动应用
cd backend && python main.py
```

---

需要更多帮助？提供完整的错误日志，我会帮您分析！
