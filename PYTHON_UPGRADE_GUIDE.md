# 🐍 Python 升级安装指南

## 当前问题

- 系统 Python 版本：3.7.6 / 3.8.2（太旧）
- 项目需要：Python 3.9+ （推荐 3.10）
- Homebrew 版本较旧且需要权限修复

---

## ✅ 推荐方案：从官网下载安装（最简单可靠）

### 步骤 1：下载 Python 3.10

1. **访问 Python 官网**：
   ```
   https://www.python.org/downloads/macos/
   ```

2. **下载 Python 3.10.x**（推荐选择 3.10.13 或更新版本）
   - 找到 "Python 3.10.x" 
   - 点击 "Download macOS 64-bit universal2 installer"
   - 文件名类似：`python-3.10.13-macos11.pkg`

### 步骤 2：安装 Python

1. **双击下载的 `.pkg` 文件**
2. **按照安装向导操作**
   - 点击"继续"
   - 同意许可协议
   - 选择安装位置（使用默认即可）
   - 输入管理员密码
   - 等待安装完成

3. **验证安装**
   ```bash
   /usr/local/bin/python3.10 --version
   # 应该显示：Python 3.10.x
   ```

### 步骤 3：创建虚拟环境

```bash
# 进入项目目录
cd /Users/feifei/work/self-interest/bestwishes

# 删除旧的虚拟环境（如果存在）
rm -rf venv

# 使用 Python 3.10 创建新的虚拟环境
/usr/local/bin/python3.10 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 验证 Python 版本
python --version
# 应该显示：Python 3.10.x
```

### 步骤 4：升级 pip 并安装依赖

```bash
# 确保虚拟环境已激活（提示符前有 (venv)）
source venv/bin/activate

# 升级 pip
pip install --upgrade pip

# 安装项目依赖
cd backend
pip install -r requirements.txt

# 说明：
# - 安装过程需要 5-10 分钟
# - 首次会下载并编译一些包
# - PyTorch 较大（约 1-2 GB）
```

### 步骤 5：启动应用

```bash
# 确保在 backend 目录且虚拟环境已激活
cd /Users/feifei/work/self-interest/bestwishes/backend
source ../venv/bin/activate

# 启动应用
python main.py

# 或使用 uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 步骤 6：访问应用

打开浏览器访问：
```
http://localhost:8000
```

---

## 方案 2：修复 Homebrew 后安装（需要管理员权限）

### 2.1 修复 Homebrew 权限

```bash
# 修复 Cellar 权限
sudo chown -R $(whoami) /usr/local/Cellar

# 修复整个 /usr/local 权限
sudo chown -R $(whoami) /usr/local/*

# 更新 Homebrew
brew update
```

### 2.2 安装 Python 3.10

```bash
# 更新后尝试安装
brew install python@3.10

# 如果还是没有 python@3.10，尝试
brew install python@3.11
# 或
brew install python3
```

### 2.3 后续步骤

按照"方案 1"的步骤 3-6 操作，但使用：
```bash
# 查找 Homebrew 安装的 Python 路径
which python3.10
# 或
ls /usr/local/opt/python*/bin/python3*

# 使用该路径创建虚拟环境
/usr/local/opt/python@3.10/bin/python3.10 -m venv venv
```

---

## 方案 3：使用在线云环境（无需本地安装）

如果本地安装困难，可以使用云环境：

### Google Colab（免费）

1. 访问 https://colab.research.google.com/
2. 上传项目文件
3. 使用 GPU 加速（比本地 CPU 快很多）

### Kaggle Notebooks（免费）

1. 访问 https://www.kaggle.com/
2. 创建新的 Notebook
3. 启用 GPU

---

## 一键安装脚本（推荐从官网安装后使用）

安装 Python 3.10 后，运行此脚本自动配置环境：

```bash
#!/bin/bash

echo "🚀 开始配置语音克隆应用环境..."

# 项目目录
PROJECT_DIR="/Users/feifei/work/self-interest/bestwishes"
cd "$PROJECT_DIR"

# 查找 Python 3.10
PYTHON310=""
for py in /usr/local/bin/python3.10 /usr/local/opt/python@3.10/bin/python3.10 /Library/Frameworks/Python.framework/Versions/3.10/bin/python3.10; do
    if [ -f "$py" ]; then
        PYTHON310="$py"
        break
    fi
done

if [ -z "$PYTHON310" ]; then
    echo "❌ 未找到 Python 3.10"
    echo "请先从官网下载安装：https://www.python.org/downloads/"
    exit 1
fi

echo "✅ 找到 Python: $PYTHON310"
$PYTHON310 --version

# 删除旧环境
echo "🧹 清理旧环境..."
rm -rf venv

# 创建虚拟环境
echo "📦 创建虚拟环境..."
$PYTHON310 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 升级 pip
echo "⬆️  升级 pip..."
pip install --upgrade pip

# 安装依赖
echo "📥 安装依赖（需要 5-10 分钟）..."
cd backend
pip install -r requirements.txt

echo ""
echo "✅ 安装完成！"
echo ""
echo "🚀 启动应用："
echo "   cd /Users/feifei/work/self-interest/bestwishes"
echo "   source venv/bin/activate"
echo "   cd backend"
echo "   python main.py"
echo ""
echo "然后访问：http://localhost:8000"
```

将上述脚本保存为 `setup.sh`，然后运行：

```bash
chmod +x setup.sh
./setup.sh
```

---

## 验证安装

运行测试脚本检查环境：

```bash
cd /Users/feifei/work/self-interest/bestwishes
source venv/bin/activate
python test_setup.py
```

---

## 常见问题

### Q1: 安装依赖时出现编译错误

**问题**：某些包需要编译但缺少工具

**解决**：
```bash
# 安装 Xcode Command Line Tools
xcode-select --install

# 或安装完整 Xcode（从 App Store）
```

### Q2: 安装 PyTorch 很慢

**解决**：使用国内镜像
```bash
pip install torch torchaudio -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q3: 提示缺少 ffmpeg

**问题**：音频处理需要 ffmpeg

**解决**：
```bash
# 使用 Homebrew 安装（如果可用）
brew install ffmpeg

# 或从官网下载：https://ffmpeg.org/download.html
```

### Q4: 安装 TTS 失败

**解决**：
```bash
# 单独安装 TTS
pip install TTS --no-deps
pip install -r requirements.txt
```

### Q5: 虚拟环境激活后 Python 版本仍然是旧的

**问题**：虚拟环境创建时使用了错误的 Python

**解决**：
```bash
# 删除虚拟环境
rm -rf venv

# 使用完整路径重新创建
/usr/local/bin/python3.10 -m venv venv

# 重新激活
source venv/bin/activate
python --version  # 确认版本
```

---

## 推荐流程总结

1. **从 Python 官网下载安装 3.10** ⭐⭐⭐⭐⭐（最推荐）
   - 最可靠
   - 无需修复 Homebrew
   - 官方支持

2. **使用一键脚本配置环境**
   - 自动化所有步骤
   - 减少出错

3. **运行 test_setup.py 验证**
   - 确保所有依赖正确

4. **启动应用**
   - 首次运行会下载模型

---

## 下载链接速查

- **Python 3.10 官方下载**：https://www.python.org/downloads/macos/
- **Xcode Command Line Tools**：运行 `xcode-select --install`
- **ffmpeg**：https://ffmpeg.org/download.html

---

## 需要帮助？

如果遇到问题：
1. 查看上面的"常见问题"
2. 运行 `python test_setup.py` 获取详细错误
3. 查看完整错误信息后再解决

---

🎉 **祝您安装顺利！**
