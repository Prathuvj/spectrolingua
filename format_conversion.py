import librosa
import soundfile as sf
import tempfile
import os
from typing import BinaryIO


class AudioConverter:
    SUPPORTED_FORMATS = ['mp3', 'mp4', 'wav', 'flac', 'aac', 'ogg', 'wma', 'm4a', 'aiff']
    
    @staticmethod
    def convert_to_wav(audio_file: BinaryIO, original_filename: str) -> bytes:
        file_extension = original_filename.split('.')[-1].lower()
        
        if file_extension not in AudioConverter.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported audio format: {file_extension}")
        
        with tempfile.NamedTemporaryFile(suffix=f'.{file_extension}', delete=False) as temp_input:
            temp_input.write(audio_file.read())
            temp_input_path = temp_input.name
        
        try:
            audio_data, sample_rate = librosa.load(temp_input_path, sr=None)
            
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_output:
                temp_output_path = temp_output.name
            
            sf.write(temp_output_path, audio_data, sample_rate, format='WAV')
            
            with open(temp_output_path, 'rb') as wav_file:
                wav_data = wav_file.read()
            
            os.unlink(temp_output_path)
            return wav_data
            
        finally:
            os.unlink(temp_input_path)
    
    @staticmethod
    def get_supported_formats():
        return AudioConverter.SUPPORTED_FORMATS