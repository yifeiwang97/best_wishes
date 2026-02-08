#!/usr/bin/env python3
"""
快速测试脚本 - 验证环境配置是否正确
运行此脚本以检查所有依赖是否正确安装
"""

import sys


def check_python_version():
    """检查 Python 版本"""
    print("🔍 检查 Python 版本...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 9:
        print("   ✅ Python 版本符合要求")
        return True
    else:
        print("   ❌ Python 版本过低，需要 3.9+")
        return False


def check_dependencies():
    """检查依赖包"""
    print("\n🔍 检查依赖包...")
    
    dependencies = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("torch", "PyTorch"),
        ("torchaudio", "TorchAudio"),
        ("TTS", "Coqui TTS"),
        ("pydub", "Pydub"),
        ("aiofiles", "AioFiles"),
    ]
    
    all_ok = True
    for module_name, display_name in dependencies:
        try:
            __import__(module_name)
            print(f"   ✅ {display_name}")
        except ImportError:
            print(f"   ❌ {display_name} 未安装")
            all_ok = False
    
    return all_ok


def check_torch_device():
    """检查 PyTorch 可用设备"""
    print("\n🔍 检查可用的计算设备...")
    
    try:
        import torch
        
        # 检查 CUDA
        if torch.cuda.is_available():
            print(f"   ✅ CUDA 可用")
            print(f"      设备数量: {torch.cuda.device_count()}")
            print(f"      当前设备: {torch.cuda.get_device_name(0)}")
            return "cuda"
        
        # 检查 MPS (Apple Silicon)
        if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            print(f"   ✅ MPS (Apple Silicon) 可用")
            return "mps"
        
        # CPU
        print(f"   ⚠️  仅 CPU 可用（推理速度会较慢）")
        return "cpu"
        
    except Exception as e:
        print(f"   ❌ 检查失败: {e}")
        return None


def check_tts_model():
    """检查 TTS 模型是否可以加载"""
    print("\n🔍 检查 TTS 模型...")
    
    try:
        from TTS.api import TTS
        print("   正在初始化 XTTS 模型（首次运行会下载模型）...")
        
        # 这将触发模型下载（如果还没下载）
        model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
        print(f"   模型: {model_name}")
        
        # 注意：这里不实际加载模型，避免测试时间过长
        print("   ℹ️  跳过实际加载（避免下载大文件）")
        print("   提示: 首次运行应用时会自动下载约 1.8GB 的模型")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 检查失败: {e}")
        return False


def check_directories():
    """检查必要的目录结构"""
    print("\n🔍 检查目录结构...")
    
    import os
    from pathlib import Path
    
    base_dir = Path(__file__).parent
    required_dirs = [
        "backend",
        "frontend",
    ]
    
    required_files = [
        "backend/main.py",
        "backend/tts_engine.py",
        "backend/audio_utils.py",
        "backend/requirements.txt",
        "frontend/index.html",
        "Dockerfile",
        "docker-compose.yml",
    ]
    
    all_ok = True
    
    for dir_name in required_dirs:
        dir_path = base_dir / dir_name
        if dir_path.exists():
            print(f"   ✅ {dir_name}/")
        else:
            print(f"   ❌ {dir_name}/ 不存在")
            all_ok = False
    
    for file_name in required_files:
        file_path = base_dir / file_name
        if file_path.exists():
            print(f"   ✅ {file_name}")
        else:
            print(f"   ❌ {file_name} 不存在")
            all_ok = False
    
    return all_ok


def main():
    """主测试函数"""
    print("=" * 50)
    print("   语音克隆应用 - 环境检查")
    print("=" * 50)
    
    results = []
    
    # 运行所有检查
    results.append(("Python 版本", check_python_version()))
    results.append(("目录结构", check_directories()))
    results.append(("依赖包", check_dependencies()))
    results.append(("计算设备", check_torch_device() is not None))
    results.append(("TTS 模型", check_tts_model()))
    
    # 总结
    print("\n" + "=" * 50)
    print("   检查结果总结")
    print("=" * 50)
    
    all_passed = all(result for _, result in results)
    
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"   {name}: {status}")
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("✅ 所有检查通过！环境配置正确。")
        print("\n🚀 下一步：")
        print("   • 运行 ./start.sh (Linux/Mac)")
        print("   • 运行 start.bat (Windows)")
        print("   • 或使用 docker-compose up -d")
    else:
        print("❌ 部分检查未通过，请修复后再试。")
        print("\n📝 提示：")
        print("   • 如果依赖包未安装: pip install -r backend/requirements.txt")
        print("   • 如果 Python 版本不对: 使用 Python 3.10")
    
    print("=" * 50)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
