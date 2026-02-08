"""
XTTS 语音合成引擎封装
提供基于 Coqui TTS 的语音克隆功能
"""

import os
import torch
from TTS.api import TTS
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TTSEngine:
    """XTTS 语音合成引擎"""
    
    def __init__(self):
        self.tts = None
        self.device = None
        self.model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
        
    def initialize(self):
        """初始化 TTS 模型（延迟加载）"""
        if self.tts is not None:
            return
        
        logger.info("正在初始化 XTTS 模型...")
        
        # 自动选择设备
        if torch.cuda.is_available():
            self.device = "cuda"
            logger.info("使用 CUDA 加速")
        elif torch.backends.mps.is_available():
            self.device = "mps"
            logger.info("使用 Apple Silicon MPS 加速")
        else:
            self.device = "cpu"
            logger.info("使用 CPU（速度较慢，建议使用 GPU）")
        
        # 加载模型
        try:
            self.tts = TTS(self.model_name).to(self.device)
            logger.info("XTTS 模型加载成功")
        except Exception as e:
            logger.error(f"模型加载失败: {str(e)}")
            raise
    
    def synthesize(
        self,
        text: str,
        speaker_wav: str,
        output_path: str,
        language: str = "zh-cn"
    ) -> str:
        """
        合成语音
        
        Args:
            text: 要合成的文本
            speaker_wav: 参考音频路径（用于克隆音色）
            output_path: 输出音频路径
            language: 语言代码（zh-cn, en, ja 等）
        
        Returns:
            输出音频文件路径
        """
        # 确保模型已加载
        if self.tts is None:
            self.initialize()
        
        # 验证参考音频
        if not os.path.exists(speaker_wav):
            raise FileNotFoundError(f"参考音频文件不存在: {speaker_wav}")
        
        # 确保输出目录存在
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"开始合成语音...")
        logger.info(f"  文本: {text[:50]}...")
        logger.info(f"  参考音频: {speaker_wav}")
        logger.info(f"  语言: {language}")
        
        try:
            # 调用 XTTS 进行语音合成
            self.tts.tts_to_file(
                text=text,
                file_path=output_path,
                speaker_wav=speaker_wav,
                language=language,
                split_sentences=True  # 自动分句，提高长文本效果
            )
            
            logger.info(f"语音合成成功: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"语音合成失败: {str(e)}")
            raise
    
    def get_supported_languages(self) -> list:
        """获取支持的语言列表"""
        return [
            "en",      # 英语
            "es",      # 西班牙语
            "fr",      # 法语
            "de",      # 德语
            "it",      # 意大利语
            "pt",      # 葡萄牙语
            "pl",      # 波兰语
            "tr",      # 土耳其语
            "ru",      # 俄语
            "nl",      # 荷兰语
            "cs",      # 捷克语
            "ar",      # 阿拉伯语
            "zh-cn",   # 中文
            "ja",      # 日语
            "hu",      # 匈牙利语
            "ko",      # 韩语
            "hi",      # 印地语
        ]


# 全局单例
_engine = None


def get_engine() -> TTSEngine:
    """获取 TTS 引擎单例"""
    global _engine
    if _engine is None:
        _engine = TTSEngine()
    return _engine
