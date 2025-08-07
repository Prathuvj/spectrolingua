import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import tempfile
import os
from typing import BinaryIO
import io


class SpectrogramGenerator:
    
    @staticmethod
    def generate_spectrogram(audio_data: bytes, sample_rate: int = None) -> bytes:
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_file.write(audio_data)
            temp_file_path = temp_file.name
        
        try:
            y, sr = librosa.load(temp_file_path, sr=sample_rate)
            
            D = librosa.stft(y)
            S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
            
            plt.figure(figsize=(14, 8))
            librosa.display.specshow(
                S_db, 
                sr=sr, 
                x_axis='time', 
                y_axis='log',
                cmap='viridis'
            )
            plt.colorbar(format='%+2.0f dB')
            plt.title('STFT Spectrogram (Log-Frequency Scale)')
            plt.xlabel('Time (seconds)')
            plt.ylabel('Frequency (Hz)')
            plt.tight_layout()
            
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            
            plt.close()
            
            return img_buffer.getvalue()
            
        finally:
            os.unlink(temp_file_path)
    
    @staticmethod
    def generate_spectrogram_from_file(audio_file: BinaryIO, original_filename: str) -> bytes:
        file_extension = original_filename.split('.')[-1].lower()
        
        with tempfile.NamedTemporaryFile(suffix=f'.{file_extension}', delete=False) as temp_input:
            temp_input.write(audio_file.read())
            temp_input_path = temp_input.name
        
        try:
            y, sr = librosa.load(temp_input_path, sr=None)
            
            D = librosa.stft(y, hop_length=512, n_fft=2048)
            S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
            
            plt.figure(figsize=(14, 8))
            librosa.display.specshow(
                S_db, 
                sr=sr, 
                hop_length=512,
                x_axis='time', 
                y_axis='log',
                cmap='viridis',
                fmin=20,
                fmax=sr//2
            )
            plt.colorbar(format='%+2.0f dB', label='Magnitude (dB)')
            plt.title(f'STFT Spectrogram - {original_filename} (Log-Frequency Scale)')
            plt.xlabel('Time (seconds)')
            plt.ylabel('Frequency (Hz)')
            plt.tight_layout()
            
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            
            plt.close()
            
            return img_buffer.getvalue()
            
        finally:
            os.unlink(temp_input_path)