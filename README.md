# 🎙️ 语音克隆应用

基于 Coqui XTTS 零样本语音克隆技术的本地部署应用。用户只需上传参考音频（3秒即可）和输入目标文字，即可生成克隆该音色的合成语音。

## ✨ 特性

- 🚀 **零样本克隆**：仅需 3-30 秒参考音频，无需训练
- 🌍 **多语言支持**：支持中、英、日、韩等 17 种语言
- 💻 **跨平台部署**：Mac（支持 Apple Silicon MPS）、Linux、Windows
- 🎨 **现代化 UI**：简洁美观的 Web 界面
- 🐳 **Docker 支持**：一键部署，开箱即用
- ⚡ **GPU 加速**：支持 CUDA、MPS（Apple Silicon）加速

## 📋 系统要求

### 硬件要求
- **内存**：建议 8GB+ RAM
- **存储**：约 5GB（包括模型和依赖）
- **GPU**：可选（有 GPU 可显著提升速度）
  - NVIDIA GPU：支持 CUDA
  - Apple Silicon (M1/M2/M3)：支持 MPS 加速
  - 无 GPU：使用 CPU（速度较慢）

### 软件要求
- Python 3.10（本地部署）
- Docker & Docker Compose（Docker 部署）

## 🚀 快速开始

### 方式一：Docker 部署（推荐）

最简单的部署方式，适合生产环境。

```bash
# 1. 克隆项目
git clone <repository-url>
cd bestwishes

# 2. 启动服务
docker-compose up -d

# 3. 访问应用
# 打开浏览器访问 http://localhost:8000
```

**首次启动说明**：首次运行会自动下载 XTTS 模型（约 1.8GB），请耐心等待 5-10 分钟。模型会缓存在 `./models` 目录，后续启动无需重新下载。

```bash
# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 完全清理（包括缓存的模型）
docker-compose down -v
```

### 方式二：本地 Python 部署

适合开发调试。

```bash
# 1. 创建虚拟环境（推荐使用 Python 3.10）
python3.10 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 安装依赖
cd backend
pip install -r requirements.txt

# 3. 启动服务
python main.py

# 或使用 uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

访问 http://localhost:8000 即可使用。

## 📖 使用指南

### 1. 准备参考音频

参考音频质量直接影响克隆效果：

- **时长**：3-30 秒（推荐 5-10 秒）
- **质量**：清晰无背景噪音
- **格式**：支持 wav、mp3、m4a、flac、ogg
- **内容**：与目标语言一致效果更好

### 2. 使用 Web 界面

1. 打开浏览器访问 http://localhost:8000
2. 上传参考音频文件（拖拽或点击选择）
3. 输入要合成的文字（最多 5000 字符）
4. 选择目标语言（默认中文）
5. 点击"开始合成"
6. 等待合成完成，播放或下载音频

### 3. 使用 API

应用也提供 REST API 接口：

```bash
# 合成语音
curl -X POST http://localhost:8000/api/synthesize \
  -F "text=你好，这是一个语音克隆测试。" \
  -F "voice_file=@reference.wav" \
  -F "language=zh-cn" \
  --output output.wav

# 获取支持的语言列表
curl http://localhost:8000/api/languages

# 健康检查
curl http://localhost:8000/health
```

完整 API 文档：访问 http://localhost:8000/docs

## 🏗️ 项目结构

```
bestwishes/
├── backend/                 # 后端代码
│   ├── main.py             # FastAPI 应用入口
│   ├── tts_engine.py       # XTTS 引擎封装
│   ├── audio_utils.py      # 音频预处理工具
│   └── requirements.txt    # Python 依赖
├── frontend/               # 前端代码
│   └── index.html          # Web UI 界面
├── uploads/                # 上传文件临时目录（自动创建）
├── outputs/                # 生成音频输出目录（自动创建）
├── models/                 # 模型缓存目录（自动创建）
├── Dockerfile              # Docker 镜像定义
├── docker-compose.yml      # Docker Compose 配置
└── README.md               # 项目文档
```

## 🔧 配置说明

### 环境变量

在 `docker-compose.yml` 或本地环境中可配置：

- `COQUI_TOS_AGREED=1`：同意 Coqui TTS 服务条款（必需）

### 端口配置

默认端口 8000，可在 `docker-compose.yml` 中修改：

```yaml
ports:
  - "8080:8000"  # 将服务映射到主机的 8080 端口
```

### GPU 支持

**NVIDIA GPU**（Linux）：

在 `docker-compose.yml` 中取消注释：

```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: 1
          capabilities: [gpu]
```

需要预先安装 [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)。

**Apple Silicon MPS**：

本地部署时自动检测并使用 MPS 加速，无需额外配置。

## 🌐 支持的语言

| 语言代码 | 语言名称 | 语言代码 | 语言名称 |
|---------|---------|---------|---------|
| zh-cn   | 中文     | en      | English |
| ja      | 日本語   | ko      | 한국어   |
| es      | Español | fr      | Français |
| de      | Deutsch | it      | Italiano |
| pt      | Português | ru    | Русский |
| ar      | العربية | hi      | हिन्दी |
| tr      | Türkçe  | pl      | Polski  |
| nl      | Nederlands | cs   | Čeština |
| hu      | Magyar  |         |         |

## 🛠️ 常见问题

### Q: 首次启动很慢？
A: 首次运行需要下载约 1.8GB 的 XTTS 模型，请耐心等待。模型会缓存，后续启动很快。

### Q: 生成速度慢？
A: 
- CPU 推理较慢，建议使用 GPU
- Mac 用户会自动使用 MPS 加速
- 可以减少文本长度，分段合成

### Q: 中文效果不佳？
A: 
- 确保参考音频为中文
- 避免使用复杂的专业术语或缩写
- 可尝试调整参考音频的长度和质量

### Q: 内存不足？
A: 
- 关闭其他占用内存的程序
- 减少文本长度
- 使用更大内存的机器

### Q: Docker 容器无法启动？
A: 
- 检查端口 8000 是否被占用
- 查看日志：`docker-compose logs`
- 确保 Docker 有足够的内存分配（建议 8GB+）

## 🔒 隐私与安全

- **本地部署**：所有数据处理均在本地进行，不上传云端
- **临时文件**：上传的音频和生成的文件存储在本地，可定期清理
- **清理接口**：提供 `/api/cleanup` 接口清理超过 24 小时的临时文件

```bash
# 清理旧文件
curl -X DELETE "http://localhost:8000/api/cleanup?max_age_hours=24"
```

## 📚 技术栈

- **后端**：FastAPI + Python 3.10
- **TTS 引擎**：Coqui TTS (XTTS v2)
- **音频处理**：torchaudio + pydub
- **深度学习**：PyTorch
- **前端**：原生 HTML/CSS/JavaScript
- **部署**：Docker + Docker Compose

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目使用 MIT 许可证。Coqui TTS 使用 MPL 2.0 许可证。

## 🙏 致谢

- [Coqui TTS](https://github.com/coqui-ai/TTS) - 提供优秀的 TTS 引擎
- [XTTS](https://docs.coqui.ai/en/latest/models/xtts.html) - 零样本语音克隆模型

## 📮 联系方式

如有问题或建议，欢迎提交 Issue。

---

**⚠️ 重要提示**：请负责任地使用语音克隆技术，仅用于授权的合法用途。未经许可克隆他人声音可能涉及法律和道德问题。
# best_wishes
