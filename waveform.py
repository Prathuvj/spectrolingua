import librosa
import matplotlib.pyplot as plt
import numpy as np
import tempfile
import os
from typing import BinaryIO
import io
import base64


class WaveformGenerator:
    
    @staticmethod
    def generate_waveform(audio_data: bytes, sample_rate: int = None) -> bytes:
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_file.write(audio_data)
            temp_file_path = temp_file.name
        
        try:
            y, sr = librosa.load(temp_file_path, sr=sample_rate)
            
            plt.figure(figsize=(12, 6))
            plt.plot(np.linspace(0, len(y)/sr, len(y)), y)
            plt.title('Audio Waveform')
            plt.xlabel('Time (seconds)')
            plt.ylabel('Amplitude')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            
            plt.close()
            
            return img_buffer.getvalue()
            
        finally:
            os.unlink(temp_file_path)
    
    @staticmethod
    def generate_waveform_from_file(audio_file: BinaryIO, original_filename: str) -> bytes:
        file_extension = original_filename.split('.')[-1].lower()
        
        with tempfile.NamedTemporaryFile(suffix=f'.{file_extension}', delete=False) as temp_input:
            temp_input.write(audio_file.read())
            temp_input_path = temp_input.name
        
        try:
            y, sr = librosa.load(temp_input_path, sr=None)
            
            plt.figure(figsize=(12, 6))
            plt.plot(np.linspace(0, len(y)/sr, len(y)), y)
            plt.title(f'Audio Waveform - {original_filename}')
            plt.xlabel('Time (seconds)')
            plt.ylabel('Amplitude')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            
            plt.close()
            
            return img_buffer.getvalue()
            
        finally:
            os.unlink(temp_input_path)