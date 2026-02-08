# ✅ 安装成功指南

本文档记录了经过实际验证的安装步骤和解决方案。

## 🎉 已验证的安装流程

以下是经过实际测试、成功运行的完整流程：

---

## 环境信息

- **操作系统**：macOS 11.7.10
- **系统 Python**：3.7.6 / 3.8.2（太旧，不可用）
- **安装 Python**：3.10.x（从官网下载安装）
- **Homebrew**：已安装但版本较旧

---

## 完整安装步骤

### 第一步：安装 Python 3.10

1. **下载 Python 3.10**
   - 访问：https://www.python.org/downloads/macos/
   - 下载：Python 3.10.13 macOS 64-bit universal2 installer
   - 文件名：`python-3.10.13-macos11.pkg`

2. **安装**
   - 双击 `.pkg` 文件
   - 按照安装向导操作
   - 完成后验证：
   ```bash
   /usr/local/bin/python3.10 --version
   # 输出：Python 3.10.13
   ```

### 第二步：创建虚拟环境

```bash
cd /Users/feifei/work/self-interest/bestwishes

# 使用 Python 3.10 创建虚拟环境
/usr/local/bin/python3.10 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 验证版本
python --version
# 应显示：Python 3.10.x
```

### 第三步：解决 SSL 证书问题

macOS 11.7.10 存在 SSL 证书验证问题，需要使用信任主机选项：

```bash
# 升级 pip
pip install --upgrade pip setuptools wheel --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

### 第四步：安装依赖

#### 方法 A：使用修复脚本（推荐）

```bash
# 确保虚拟环境已激活
source venv/bin/activate

# 运行修复脚本
./fix_install.sh
```

#### 方法 B：手动安装（如果脚本失败）

```bash
cd backend

# 1. 安装基础包
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org "numpy<2.0.0"

# 2. 安装 PyTorch（CPU 版本）
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org torch==2.1.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cpu

# 3. 尝试安装 numba（可能失败，没关系）
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org llvmlite==0.40.1 numba==0.57.1 || echo "跳过 numba"

# 4. 安装 TTS
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org TTS==0.22.0 --no-deps

# 5. 安装 TTS 依赖
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org \
    coqpit scipy librosa soundfile inflect pypinyin jieba pandas requests tqdm \
    packaging pyyaml fsspec einops transformers encodec aiohttp anyascii \
    cython flask matplotlib nltk num2words pysbd unidecode trainer

# 6. 安装项目依赖
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org \
    fastapi==0.109.0 uvicorn[standard]==0.27.0 python-multipart==0.0.6 \
    aiofiles==23.2.1 pydub==0.25.1
```

### 第五步：验证安装

```bash
cd /Users/feifei/work/self-interest/bestwishes
source venv/bin/activate

# 测试导入
python -c "from TTS.api import TTS; print('✅ TTS 导入成功')"

# 运行完整测试
python test_setup.py
```

### 第六步：启动应用

```bash
cd backend
python main.py
```

**成功标志**：
```
INFO:     Uvicorn running on http://0.0.0.0:8000
 > tts_models/multilingual/multi-dataset/xtts_v2 is already downloaded.
正在初始化 XTTS 模型...
XTTS 模型加载成功
```

### 第七步：测试应用

1. 打开浏览器访问：http://localhost:8000
2. 上传一个参考音频（5-10 秒，wav 或 mp3）
3. 输入测试文字："你好，这是语音克隆测试。"
4. 点击"开始合成"
5. 等待几秒到几十秒
6. 播放或下载合成的音频

**成功！** 🎉

---

## 遇到的问题和解决方案

### 问题 1：`No module named 'fastapi'`

**原因**：系统 Python 版本太旧（3.7/3.8）

**解决**：安装 Python 3.10 并创建虚拟环境

### 问题 2：SSL 证书验证错误

**错误信息**：
```
SSLError(SSLCertVerificationError('OSStatus -26276'))
```

**解决**：使用 `--trusted-host` 选项
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org <包名>
```

### 问题 3：numba/llvmlite 编译失败

**错误信息**：
```
Failed to build installable wheels for some pyproject.toml based projects
╰─> numba, llvmlite
```

**解决**：跳过这些包（不影响核心功能）
```bash
# 使用修复脚本自动处理
./fix_install.sh
```

### 问题 4：缺少 coqpit 模块

**错误信息**：
```
No module named 'coqpit'
```

**解决**：
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org coqpit
```

### 问题 5：transformers 导入错误

**错误信息**：
```
cannot import name 'BeamSearchScorer' from 'transformers'
```

**解决**：安装 TTS 的所有依赖（修复脚本已包含）

---

## 关键要点

### ✅ 必需的

1. **Python 3.10+**：系统自带的 3.7/3.8 太旧
2. **虚拟环境**：避免污染系统 Python
3. **--trusted-host**：解决 SSL 证书问题
4. **完整依赖**：TTS 有大量依赖，需要全部安装

### ⚠️ 可选的

1. **numba**：编译可能失败，但不影响核心功能
2. **GPU**：没有 GPU 也能运行，只是慢一些
3. **某些语言包**：如 bangla, gruut 等（不用中文/英文可跳过）

### 💡 建议

1. **使用修复脚本**：`./fix_install.sh` 已经处理了所有已知问题
2. **首次启动耐心**：模型下载需要 5-10 分钟
3. **遇到问题查看日志**：错误信息通常能指明问题所在

---

## 性能参考

**测试环境**：
- CPU: Intel（具体型号未知）
- 内存: 8GB+
- 系统: macOS 11.7.10

**性能表现**：
- 首次启动：约 30 秒（模型已下载）
- 10 字文本合成：约 15-20 秒（CPU）
- 50 字文本合成：约 60-90 秒（CPU）

**优化建议**：
- 使用 GPU 可提升 3-5 倍速度
- Apple Silicon (M1/M2) 使用 MPS 加速
- 分段合成长文本效果更好

---

## 文件清单

安装成功后的项目结构：

```
bestwishes/
├── venv/                           # 虚拟环境
├── backend/                        # 后端代码
│   ├── main.py
│   ├── tts_engine.py
│   ├── audio_utils.py
│   └── requirements.txt
├── frontend/                       # 前端页面
│   └── index.html
├── uploads/                        # 上传的音频（运行时创建）
├── outputs/                        # 生成的音频（运行时创建）
├── setup_python.sh                 # 自动配置脚本
├── fix_install.sh                  # 修复安装脚本
├── test_setup.py                   # 环境测试脚本
└── README.md                       # 主文档
```

---

## 下一步

应用成功运行后，您可以：

1. **尝试不同的音色**：上传不同的参考音频
2. **测试多种语言**：支持中、英、日、韩等 17 种语言
3. **调整参考音频**：5-10 秒清晰音频效果最佳
4. **查看 API 文档**：http://localhost:8000/docs
5. **阅读使用指南**：查看 QUICKSTART.md

---

## 反馈

如果您在安装过程中遇到任何问题：

1. 查看本文档的"遇到的问题和解决方案"部分
2. 运行 `python test_setup.py` 获取详细诊断
3. 查看 TROUBLESHOOTING.md 获取更多解决方案
4. 提交 Issue 并附上错误日志

---

**恭喜您成功安装和运行语音克隆应用！** 🎊
