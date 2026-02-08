# 🚀 快速入门指南

5 分钟上手语音克隆应用！

## 📦 方式一：一键启动（最简单）

**⚠️ 重要提示**：一键启动需要 Python 3.10+ 或 Docker。

### macOS / Linux

```bash
# 进入项目目录
cd bestwishes

# 如果没有 Python 3.10，先运行配置脚本
./setup_python.sh

# 然后启动应用
./start.sh
```

### Windows

```cmd
# 进入项目目录
cd bestwishes

# 运行启动脚本
start.bat
```

启动脚本会自动检测您的环境并选择最佳部署方式。

**如果遇到问题**：
- 检查 Python 版本：`python --version`（需要 3.10+）
- 或使用 Docker：`docker-compose up -d`

## 🐳 方式二：Docker 部署（推荐）

适合生产环境，一键部署。

```bash
# 1. 启动服务
docker-compose up -d

# 2. 查看日志（可选）
docker-compose logs -f

# 3. 打开浏览器
# 访问 http://localhost:8000
```

**首次启动提示**：首次运行会自动下载约 1.8GB 的 XTTS 模型，请耐心等待 5-10 分钟。

## 💻 方式三：本地 Python 部署（需要 Python 3.10+）

适合开发调试。

### 快速安装（推荐）

```bash
# 1. 运行自动配置脚本
cd bestwishes
./setup_python.sh

# 脚本会自动：
# - 查找 Python 3.10+
# - 创建虚拟环境
# - 安装所有依赖
# - 运行环境检查

# 2. 启动应用
source venv/bin/activate
cd backend
python main.py
```

### 手动安装

```bash
# 1. 确保有 Python 3.10+
# 如果没有，从 https://www.python.org/downloads/ 下载安装

# 2. 创建虚拟环境
/usr/local/bin/python3.10 -m venv venv

# 3. 激活虚拟环境
source venv/bin/activate  # Windows: venv\Scripts\activate

# 4. 运行修复安装脚本（解决依赖问题）
./fix_install.sh

# 5. 启动服务
cd backend
python main.py

# 6. 打开浏览器
# 访问 http://localhost:8000
```

**常见问题**：
- SSL 错误：脚本会自动使用 `--trusted-host` 解决
- numba 编译失败：脚本会自动跳过（不影响使用）
- 缺少模块：运行 `./fix_install.sh` 安装所有依赖

## 🎯 使用步骤

### 1. 准备参考音频

- **时长**：3-30 秒（推荐 5-10 秒）
- **质量**：清晰无背景噪音
- **格式**：wav、mp3、m4a、flac、ogg 均可
- **内容**：建议与目标语言一致

### 2. 合成语音

1. 打开浏览器访问 http://localhost:8000
2. **上传参考音频**：拖拽或点击选择文件
3. **输入文字**：输入要合成的目标文字（最多 5000 字）
4. **选择语言**：从下拉菜单选择（默认中文）
5. **点击合成**：等待几秒到几十秒
6. **播放或下载**：合成完成后可在线播放或下载

### 3. 示例

**示例 1：中文语音克隆**
- 参考音频：一段 10 秒的中文演讲
- 输入文字：「欢迎使用语音克隆应用！这是一个基于深度学习的文本转语音系统。」
- 语言：中文
- 结果：生成具有参考音频音色的中文语音

**示例 2：英文语音克隆**
- 参考音频：一段 5 秒的英文录音
- 输入文字：「Welcome to the voice cloning application!」
- 语言：English
- 结果：生成具有参考音频音色的英文语音

## 🔧 环境检查

运行测试脚本检查环境配置：

```bash
python test_setup.py
```

## ❓ 常见问题

### Q1: 启动后无法访问？

**检查步骤**：
1. 确认服务正在运行：`docker-compose ps` 或检查终端输出
2. 确认端口未被占用：`lsof -i:8000`（Mac/Linux）
3. 尝试访问：http://127.0.0.1:8000

### Q2: 首次启动很慢？

**原因**：首次运行需要下载 XTTS 模型（约 1.8GB）

**解决方案**：
- 确保网络连接正常
- 耐心等待 5-10 分钟
- 查看日志确认下载进度：`docker-compose logs -f`

### Q3: 合成速度慢？

**原因**：CPU 推理较慢

**解决方案**：
- 使用 GPU（NVIDIA 或 Apple Silicon）
- 减少文本长度
- 分段合成长文本

### Q4: 合成效果不好？

**改进建议**：
- 使用更清晰的参考音频
- 增加参考音频时长（5-15 秒最佳）
- 确保参考音频语言与目标语言一致
- 避免使用有背景噪音的音频

### Q5: Docker 容器启动失败？

**检查步骤**：
1. 查看日志：`docker-compose logs`
2. 确认 Docker 有足够内存（建议 8GB+）
3. 确认端口 8000 未被占用
4. 重新构建：`docker-compose build --no-cache`

## 📚 更多信息

- **完整文档**：查看 [README.md](README.md)
- **API 文档**：访问 http://localhost:8000/docs
- **更新日志**：查看 [CHANGELOG.md](CHANGELOG.md)
- **技术细节**：查看各个模块的代码注释

## 🛑 停止服务

### Docker 部署

```bash
docker-compose down
```

### 本地 Python 部署

按 `Ctrl+C` 终止进程

## 🎉 开始使用

现在您已经准备好了！开始享受语音克隆的乐趣吧！

有问题？查看 [README.md](README.md) 的"常见问题"部分，或提交 Issue。
