# 🐳 Docker 快速部署指南

## 第一步：安装 Docker Desktop

### Mac 用户安装步骤

#### 方法 1：从官网下载（推荐）

1. **访问 Docker 官网**
   ```
   https://www.docker.com/products/docker-desktop/
   ```

2. **下载适合您 Mac 的版本**
   - **Apple Silicon (M1/M2/M3)**: 选择 "Apple Chip"
   - **Intel Mac**: 选择 "Intel Chip"

3. **安装 Docker Desktop**
   - 打开下载的 `.dmg` 文件
   - 将 Docker 图标拖到 Applications 文件夹
   - 从 Applications 启动 Docker Desktop

4. **等待 Docker 启动**
   - 首次启动需要几分钟
   - 顶部菜单栏会出现 Docker 图标
   - 图标不再闪烁表示启动完成

5. **验证安装**
   ```bash
   docker --version
   docker-compose --version
   ```

#### 方法 2：使用 Homebrew（命令行）

```bash
# 安装 Docker Desktop
brew install --cask docker

# 启动 Docker（需要手动从 Applications 启动一次）
open /Applications/Docker.app

# 等待 Docker 启动完成后验证
docker --version
```

---

## 第二步：启动语音克隆应用

### 2.1 确认 Docker 正在运行

```bash
# 检查 Docker 状态
docker ps
```

如果看到类似 `CONTAINER ID  IMAGE  COMMAND...` 的表头，说明 Docker 正常运行。

### 2.2 启动应用

```bash
# 1. 进入项目目录
cd /Users/feifei/work/self-interest/bestwishes

# 2. 构建并启动服务（首次启动）
docker-compose up -d

# 说明：
# - 首次运行会下载 Python 镜像（约 200MB）
# - 安装应用依赖（约 1-2GB）
# - 下载 XTTS 模型（约 1.8GB）
# - 总计约需要 5-15 分钟，取决于网络速度
```

### 2.3 查看启动日志

```bash
# 实时查看日志（了解启动进度）
docker-compose logs -f

# 提示：
# - 看到 "Uvicorn running on..." 表示启动成功
# - 首次启动会显示模型下载进度
# - 按 Ctrl+C 退出日志查看（不会停止服务）
```

### 2.4 访问应用

启动成功后，打开浏览器访问：

```
http://localhost:8000
```

您会看到语音克隆的 Web 界面！

---

## 第三步：使用应用

### 基本操作流程

1. **上传参考音频**
   - 点击或拖拽上传音频文件
   - 支持格式：wav, mp3, m4a, flac, ogg
   - 建议时长：5-10 秒

2. **输入目标文字**
   - 在文本框输入要合成的内容
   - 最多支持 5000 字符

3. **选择语言**
   - 从下拉菜单选择（中文/英文/日语等）

4. **开始合成**
   - 点击"开始合成"按钮
   - 等待几秒到几十秒

5. **播放/下载**
   - 在线播放合成的音频
   - 或点击下载按钮保存

---

## Docker 常用命令

### 服务管理

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看运行状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 查看最近 100 行日志
docker-compose logs --tail 100
```

### 清理和重建

```bash
# 停止并删除容器（保留模型缓存）
docker-compose down

# 完全清理（包括缓存的模型，谨慎使用）
docker-compose down -v

# 重新构建镜像（代码更新后）
docker-compose build --no-cache

# 重新构建并启动
docker-compose up -d --build
```

### 进入容器调试

```bash
# 进入运行中的容器
docker-compose exec voice-cloning bash

# 在容器内查看日志
docker-compose exec voice-cloning ls -la /app

# 退出容器
exit
```

---

## 常见问题解决

### Q1: Docker Desktop 无法启动

**问题**：Docker Desktop 图标一直闪烁或显示错误

**解决**：
1. 重启 Mac
2. 检查系统设置 → 隐私 → 完全磁盘访问权限 → 确保 Docker 已勾选
3. 重新安装 Docker Desktop

### Q2: 端口 8000 被占用

**问题**：`port is already allocated`

**解决**：
```bash
# 方法 1：修改端口
# 编辑 docker-compose.yml，将 "8000:8000" 改为 "8080:8000"

# 方法 2：停止占用端口的程序
lsof -ti:8000 | xargs kill -9
```

### Q3: 下载模型失败

**问题**：无法从 Hugging Face 下载模型

**解决**：
```bash
# 方法 1：使用镜像站点
# 在 docker-compose.yml 添加环境变量：
# environment:
#   - HF_ENDPOINT=https://hf-mirror.com

# 方法 2：手动下载模型后挂载
# 1. 手动下载 XTTS 模型到 ./models 目录
# 2. 重启容器
```

### Q4: 合成速度很慢

**问题**：生成音频需要很长时间

**原因**：Docker 容器默认使用 CPU

**解决**（如果有 NVIDIA GPU）：
```bash
# 1. 安装 NVIDIA Docker 支持
# 参考：https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html

# 2. 取消 docker-compose.yml 中 GPU 配置的注释

# 3. 重启服务
docker-compose down
docker-compose up -d
```

### Q5: 容器启动后立即退出

**问题**：`docker-compose ps` 显示容器 Exit

**解决**：
```bash
# 查看完整错误日志
docker-compose logs

# 常见原因：
# - 依赖安装失败 → 检查网络连接
# - 端口冲突 → 修改端口配置
# - 内存不足 → 增加 Docker 内存限制
```

---

## 性能优化

### 增加 Docker 内存限制

Docker Desktop → Settings → Resources → Memory

建议设置：
- 最小：8 GB
- 推荐：12 GB
- 理想：16 GB

### 使用模型缓存

首次启动后，模型会缓存在 `./models` 目录，后续启动很快。

```bash
# 查看缓存大小
du -sh models/

# 预期大小约 1.8-2 GB
```

---

## 完全卸载

如果需要完全清理：

```bash
# 1. 停止并删除容器
docker-compose down -v

# 2. 删除项目镜像
docker rmi bestwishes-voice-cloning

# 3. 清理未使用的镜像和缓存（可选）
docker system prune -a

# 4. 删除模型缓存目录（可选）
rm -rf models/
```

---

## 系统要求

- **macOS**: 10.14 或更高版本
- **内存**: 最少 8GB RAM（推荐 12GB+）
- **磁盘**: 约 5GB 可用空间
- **CPU**: Apple Silicon 或 Intel 均可

---

## 下一步

应用启动成功后：

1. 📖 查看 [README.md](README.md) 了解完整功能
2. 🚀 查看 [QUICKSTART.md](QUICKSTART.md) 快速上手
3. 📚 访问 http://localhost:8000/docs 查看 API 文档

---

## 需要帮助？

- 查看日志：`docker-compose logs -f`
- 检查状态：`docker-compose ps`
- 重启服务：`docker-compose restart`

遇到问题？查看上面的"常见问题解决"或提交 Issue。

---

🎉 **祝您使用愉快！**
