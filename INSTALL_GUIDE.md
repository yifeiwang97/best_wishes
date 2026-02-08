# 🛠️ 安装指南 - 解决 Python 版本问题

## 问题说明

遇到 `No module named 'fastapi'` 错误，根本原因是系统 Python 版本太旧（3.7/3.8），而项目需要 **Python 3.9+**（推荐 3.10）。

---

## ✅ 推荐方案：使用 Docker（最简单）

Docker 方式无需担心 Python 版本问题，一键部署即可。

### 步骤 1：安装 Docker

**Mac 用户**：
```bash
# 下载并安装 Docker Desktop for Mac
# https://www.docker.com/products/docker-desktop/

# 或使用 Homebrew
brew install --cask docker
```

### 步骤 2：启动应用

```bash
cd /Users/feifei/work/self-interest/bestwishes

# 启动服务（首次会自动下载镜像和模型）
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 步骤 3：访问应用

打开浏览器访问：http://localhost:8000

**优势**：
- ✅ 无需担心 Python 版本
- ✅ 环境隔离，不影响系统
- ✅ 一键部署，开箱即用
- ✅ 跨平台一致性

---

## 方案 2：升级 Python（适合开发）

### 2.1 使用 Homebrew 安装 Python 3.10

```bash
# 1. 安装 Homebrew（如果还没安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. 安装 Python 3.10
brew install python@3.10

# 3. 验证安装
python3.10 --version

# 4. 创建虚拟环境
cd /Users/feifei/work/self-interest/bestwishes
python3.10 -m venv venv

# 5. 激活虚拟环境
source venv/bin/activate

# 6. 升级 pip
pip install --upgrade pip

# 7. 安装依赖
cd backend
pip install -r requirements.txt

# 8. 启动应用
python main.py
```

### 2.2 从官网下载安装

1. 访问 https://www.python.org/downloads/
2. 下载 Python 3.10.x for macOS
3. 运行安装包
4. 按照上面的步骤 4-8 操作

---

## 方案 3：使用 pyenv（推荐给开发者）

pyenv 可以方便地管理多个 Python 版本。

```bash
# 1. 安装 pyenv
brew install pyenv

# 2. 配置环境变量（添加到 ~/.zshrc）
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# 3. 重新加载配置
source ~/.zshrc

# 4. 安装 Python 3.10
pyenv install 3.10.13

# 5. 设置项目 Python 版本
cd /Users/feifei/work/self-interest/bestwishes
pyenv local 3.10.13

# 6. 创建虚拟环境并安装依赖
python -m venv venv
source venv/bin/activate
cd backend
pip install -r requirements.txt

# 7. 启动应用
python main.py
```

---

## 快速对比

| 方案 | 难度 | 时间 | 推荐度 | 适用场景 |
|-----|------|------|--------|---------|
| Docker | ⭐ 简单 | 5 分钟 | ⭐⭐⭐⭐⭐ | 所有用户，尤其是快速部署 |
| Homebrew | ⭐⭐ 中等 | 10 分钟 | ⭐⭐⭐⭐ | 需要本地开发调试 |
| pyenv | ⭐⭐⭐ 较难 | 15 分钟 | ⭐⭐⭐ | 专业开发者 |

---

## 验证安装

安装完成后，运行测试脚本验证环境：

```bash
cd /Users/feifei/work/self-interest/bestwishes

# 如果使用虚拟环境，先激活
source venv/bin/activate

# 运行测试
python test_setup.py
```

---

## 常见问题

### Q: Docker 安装后无法启动？
**A**: 确保 Docker Desktop 已经启动并运行。Mac 用户需要在应用程序中启动 Docker。

### Q: Homebrew 安装很慢？
**A**: 可以使用国内镜像源：
```bash
export HOMEBREW_BREW_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git"
export HOMEBREW_CORE_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-core.git"
```

### Q: pip 安装依赖失败？
**A**: 
1. 升级 pip: `pip install --upgrade pip`
2. 使用国内镜像: `pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`
3. 分步安装：先安装 torch，再安装其他依赖

### Q: 安装 TTS 时出错？
**A**: TTS 依赖较多，可能需要：
```bash
# Mac 可能需要安装音频库
brew install portaudio
brew install ffmpeg

# 然后重新安装
pip install TTS
```

---

## 推荐方案总结

**如果您只是想快速使用应用** → 选择 **Docker**

**如果您想学习或开发** → 选择 **Homebrew 安装 Python 3.10**

**如果您经常需要切换 Python 版本** → 选择 **pyenv**

---

## 需要帮助？

如果以上方案都遇到问题，请：
1. 查看 README.md 中的"常见问题"部分
2. 运行 `docker-compose logs` 查看详细错误
3. 提交 Issue 并附上错误信息

---

**提示**：首次运行会下载约 1.8GB 的 XTTS 模型，请确保网络连接正常并耐心等待。
