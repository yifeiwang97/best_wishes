"""
语音克隆应用 - FastAPI 后端
提供语音合成 API 接口
"""

import os
import uuid
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import aiofiles

from tts_engine import get_engine
from audio_utils import preprocess_audio, validate_audio, get_audio_info

# 创建 FastAPI 应用
app = FastAPI(
    title="语音克隆应用",
    description="基于 XTTS 的零样本语音克隆服务",
    version="1.0.0"
)

# 配置 CORS（允许前端跨域访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建必要的目录
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# 挂载前端静态文件
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


@app.get("/")
async def root():
    """根路径 - 返回前端页面"""
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "语音克隆 API 服务正在运行", "docs": "/docs"}


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": "voice-cloning-api",
        "version": "1.0.0"
    }


@app.get("/api/languages")
async def get_languages():
    """获取支持的语言列表"""
    engine = get_engine()
    languages = engine.get_supported_languages()
    
    # 语言名称映射
    language_names = {
        "zh-cn": "中文",
        "en": "English",
        "ja": "日本語",
        "ko": "한국어",
        "es": "Español",
        "fr": "Français",
        "de": "Deutsch",
        "it": "Italiano",
        "pt": "Português",
        "ru": "Русский",
        "ar": "العربية",
        "hi": "हिन्दी",
        "tr": "Türkçe",
        "pl": "Polski",
        "nl": "Nederlands",
        "cs": "Čeština",
        "hu": "Magyar",
    }
    
    return {
        "languages": [
            {"code": lang, "name": language_names.get(lang, lang)}
            for lang in languages
        ]
    }


@app.post("/api/synthesize")
async def synthesize_voice(
    text: str = Form(..., description="要合成的文本"),
    voice_file: UploadFile = File(..., description="参考音频文件"),
    language: str = Form("zh-cn", description="语言代码")
):
    """
    语音合成接口
    
    接收文本和参考音频，返回合成的语音文件
    """
    try:
        # 验证输入
        if not text or len(text.strip()) == 0:
            raise HTTPException(status_code=400, detail="文本不能为空")
        
        if len(text) > 5000:
            raise HTTPException(status_code=400, detail="文本过长（最多 5000 字符）")
        
        # 验证文件类型
        allowed_extensions = {".wav", ".mp3", ".m4a", ".flac", ".ogg"}
        file_ext = Path(voice_file.filename).suffix.lower()
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的音频格式。支持的格式: {', '.join(allowed_extensions)}"
            )
        
        # 生成唯一文件名
        upload_id = str(uuid.uuid4())
        upload_path = UPLOAD_DIR / f"{upload_id}{file_ext}"
        processed_path = UPLOAD_DIR / f"{upload_id}_processed.wav"
        output_path = OUTPUT_DIR / f"{upload_id}_output.wav"
        
        # 保存上传的文件
        async with aiofiles.open(upload_path, "wb") as f:
            content = await voice_file.read()
            await f.write(content)
        
        # 验证音频文件
        is_valid, error_msg = validate_audio(str(upload_path))
        if not is_valid:
            # 清理临时文件
            upload_path.unlink(missing_ok=True)
            raise HTTPException(status_code=400, detail=f"音频文件无效: {error_msg}")
        
        # 获取音频信息
        audio_info = get_audio_info(str(upload_path))
        
        # 预处理音频
        try:
            processed_audio = preprocess_audio(str(upload_path), str(processed_path))
        except Exception as e:
            # 清理临时文件
            upload_path.unlink(missing_ok=True)
            raise HTTPException(status_code=500, detail=f"音频预处理失败: {str(e)}")
        
        # 合成语音
        try:
            engine = get_engine()
            output_file = engine.synthesize(
                text=text,
                speaker_wav=processed_audio,
                output_path=str(output_path),
                language=language
            )
        except Exception as e:
            # 清理临时文件
            upload_path.unlink(missing_ok=True)
            processed_path.unlink(missing_ok=True)
            raise HTTPException(status_code=500, detail=f"语音合成失败: {str(e)}")
        
        # 清理临时文件（保留输出文件）
        upload_path.unlink(missing_ok=True)
        processed_path.unlink(missing_ok=True)
        
        # 返回音频文件
        return FileResponse(
            path=str(output_path),
            media_type="audio/wav",
            filename=f"synthesized_{upload_id}.wav",
            headers={
                "X-Audio-Info": str(audio_info),
                "X-Text-Length": str(len(text))
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")


@app.delete("/api/cleanup")
async def cleanup_files(max_age_hours: int = 24):
    """
    清理旧文件（可选的维护接口）
    
    删除超过指定时间的临时文件
    """
    import time
    
    cleaned_count = 0
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    
    for directory in [UPLOAD_DIR, OUTPUT_DIR]:
        for file_path in directory.glob("*"):
            if file_path.is_file():
                file_age = current_time - file_path.stat().st_mtime
                if file_age > max_age_seconds:
                    file_path.unlink()
                    cleaned_count += 1
    
    return {
        "message": f"已清理 {cleaned_count} 个旧文件",
        "max_age_hours": max_age_hours
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
