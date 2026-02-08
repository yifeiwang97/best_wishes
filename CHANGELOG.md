# 更新日志

## [1.0.0] - 2024-02-08

### 新增功能
- ✨ 基于 XTTS v2 的零样本语音克隆
- 🌍 支持 17 种语言（中、英、日、韩等）
- 🎨 现代化 Web UI 界面
- 📱 响应式设计，支持移动端
- 🐳 Docker 一键部署
- 🚀 支持 CUDA、MPS（Apple Silicon）、CPU 推理
- 📁 拖拽上传音频文件
- ⚡ 异步文件处理
- 🔊 在线播放和下载合成音频
- 🛡️ 音频文件格式验证
- 📊 实时字符计数
- 🔄 音频自动预处理（重采样、单声道转换）

### API 接口
- POST `/api/synthesize` - 语音合成
- GET `/api/languages` - 获取支持的语言
- GET `/health` - 健康检查
- DELETE `/api/cleanup` - 清理临时文件

### 技术栈
- FastAPI 0.109.0
- Coqui TTS 0.22.0
- PyTorch 2.0+
- torchaudio
- Docker & Docker Compose

### 文档
- 📖 完整的 README.md
- 🚀 快速启动脚本（Linux/Windows）
- 📝 API 文档（Swagger UI）
- 🔒 隐私与安全说明

### 已知限制
- 首次运行需下载约 1.8GB 模型
- CPU 推理速度较慢
- 中文复杂词汇效果有待提升
