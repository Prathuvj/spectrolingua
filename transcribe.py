import speech_recognition as sr
import tempfile
import os
from typing import BinaryIO
import io


class AudioTranscriber:
    
    @staticmethod
    def transcribe_audio_from_file(audio_file: BinaryIO, original_filename: str, language: str = 'en-US') -> str:
        file_extension = original_filename.split('.')[-1].lower()
        
        # Only support WAV files for now to avoid ffmpeg dependency issues
        if file_extension != 'wav':
            raise ValueError(f"Currently only WAV files are supported for transcription. Please convert your {file_extension} file to WAV format using the /convert/ endpoint first.")
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_input:
            temp_input.write(audio_file.read())
            temp_input_path = temp_input.name
        
        try:
            recognizer = sr.Recognizer()
            
            with sr.AudioFile(temp_input_path) as source:
                audio_data = recognizer.record(source)
            
            try:
                text = recognizer.recognize_google(audio_data, language=language)
                return text
            except sr.UnknownValueError:
                raise ValueError("Could not understand audio - speech may be unclear or not present")
            except sr.RequestError as e:
                raise ValueError(f"Could not request results from Google Speech Recognition service: {e}")
            
        finally:
            if os.path.exists(temp_input_path):
                os.unlink(temp_input_path)
    
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