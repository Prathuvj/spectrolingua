import speech_recognition as sr
import tempfile
import os
from typing import BinaryIO
import io
from format_conversion import AudioConverter


class AudioTranscriber:
    
    @staticmethod
    def transcribe_audio_from_file(audio_file: BinaryIO, original_filename: str, language: str = 'en-US') -> str:
        file_extension = original_filename.split('.')[-1].lower()
        
        # If not WAV, convert it first using our existing AudioConverter
        if file_extension != 'wav':
            try:
                # Reset file pointer to beginning
                audio_file.seek(0)
                # Convert to WAV using our existing converter
                wav_data = AudioConverter.convert_to_wav(audio_file, original_filename)
                
                # Create temporary WAV file from converted data
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
                    temp_wav.write(wav_data)
                    temp_wav_path = temp_wav.name
                
            except Exception as e:
                raise ValueError(f"Failed to convert {file_extension} to WAV for transcription: {str(e)}")
        else:
            # For WAV files, write directly to temp file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
                temp_wav.write(audio_file.read())
                temp_wav_path = temp_wav.name
        
        try:
            recognizer = sr.Recognizer()
            
            with sr.AudioFile(temp_wav_path) as source:
                audio_data = recognizer.record(source)
            
            try:
                text = recognizer.recognize_google(audio_data, language=language)
                return text
            except sr.UnknownValueError:
                raise ValueError("Could not understand audio - speech may be unclear or not present")
            except sr.RequestError as e:
                raise ValueError(f"Could not request results from Google Speech Recognition service: {e}")
            
        finally:
            if os.path.exists(temp_wav_path):
                os.unlink(temp_wav_path)
    
    @staticmethod
    def get_supported_languages():
        return {
            'en-US': 'English (US)',
            'en-GB': 'English (UK)',
            'es-ES': 'Spanish (Spain)',
            'es-MX': 'Spanish (Mexico)',
            'fr-FR': 'French (France)',
            'de-DE': 'German (Germany)',
            'it-IT': 'Italian (Italy)',
            'pt-BR': 'Portuguese (Brazil)',
            'ru-RU': 'Russian (Russia)',
            'ja-JP': 'Japanese (Japan)',
            'ko-KR': 'Korean (South Korea)',
            'zh-CN': 'Chinese (Simplified)',
            'zh-TW': 'Chinese (Traditional)',
            'ar-SA': 'Arabic (Saudi Arabia)',
            'hi-IN': 'Hindi (India)',
            'th-TH': 'Thai (Thailand)',
            'vi-VN': 'Vietnamese (Vietnam)',
            'nl-NL': 'Dutch (Netherlands)',
            'sv-SE': 'Swedish (Sweden)',
            'da-DK': 'Danish (Denmark)',
            'no-NO': 'Norwegian (Norway)',
            'fi-FI': 'Finnish (Finland)',
            'pl-PL': 'Polish (Poland)',
            'tr-TR': 'Turkish (Turkey)',
            'he-IL': 'Hebrew (Israel)',
            'cs-CZ': 'Czech (Czech Republic)',
            'hu-HU': 'Hungarian (Hungary)',
            'ro-RO': 'Romanian (Romania)',
            'sk-SK': 'Slovak (Slovakia)',
            'bg-BG': 'Bulgarian (Bulgaria)',
            'hr-HR': 'Croatian (Croatia)',
            'sl-SI': 'Slovenian (Slovenia)',
            'et-EE': 'Estonian (Estonia)',
            'lv-LV': 'Latvian (Latvia)',
            'lt-LT': 'Lithuanian (Lithuania)',
            'uk-UA': 'Ukrainian (Ukraine)'
        }