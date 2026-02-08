"""
音频预处理工具模块
将各种格式的音频转换为 XTTS 所需的格式：16kHz 单声道 WAV
"""

import os
from pathlib import Path
import torchaudio
import torch


def preprocess_audio(input_path: str, output_path: str = None) -> str:
    """
    预处理音频文件
    
    Args:
        input_path: 输入音频文件路径
        output_path: 输出音频文件路径（可选，默认为临时文件）
    
    Returns:
        处理后的音频文件路径
    """
    # 如果没有指定输出路径，创建临时文件
    if output_path is None:
        input_file = Path(input_path)
        output_path = str(input_file.parent / f"{input_file.stem}_processed.wav")
    
    # 加载音频
    try:
        waveform, sample_rate = torchaudio.load(input_path)
    except Exception as e:
        raise ValueError(f"无法加载音频文件: {str(e)}")
    
    # 转换为单声道
    if waveform.shape[0] > 1:
        # 多声道转单声道（取平均）
        waveform = torch.mean(waveform, dim=0, keepdim=True)
    
    # 重采样到 16kHz
    if sample_rate != 16000:
        resampler = torchaudio.transforms.Resample(
            orig_freq=sample_rate,
            new_freq=16000
        )
        waveform = resampler(waveform)
        sample_rate = 16000
    
    # 保存处理后的音频
    torchaudio.save(output_path, waveform, sample_rate)
    
    return output_path


def validate_audio(file_path: str) -> tuple[bool, str]:
    """
    验证音频文件是否有效
    
    Args:
        file_path: 音频文件路径
    
    Returns:
        (是否有效, 错误信息)
    """
    if not os.path.exists(file_path):
        return False, "文件不存在"
    
    try:
        waveform, sample_rate = torchaudio.load(file_path)
        
        # 检查音频长度（至少 1 秒，最多 60 秒）
        duration = waveform.shape[1] / sample_rate
        if duration < 1:
            return False, "音频时长太短（至少需要 1 秒）"
        if duration > 60:
            return False, "音频时长太长（最多 60 秒）"
        
        return True, ""
    except Exception as e:
        return False, f"音频文件无效: {str(e)}"


def get_audio_info(file_path: str) -> dict:
    """
    获取音频文件信息
    
    Args:
        file_path: 音频文件路径
    
    Returns:
        包含音频信息的字典
    """
    try:
        waveform, sample_rate = torchaudio.load(file_path)
        duration = waveform.shape[1] / sample_rate
        
        return {
            "sample_rate": sample_rate,
            "channels": waveform.shape[0],
            "duration": round(duration, 2),
            "samples": waveform.shape[1]
        }
    except Exception as e:
        return {"error": str(e)}
