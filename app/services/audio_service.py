import base64
import os
import io
from typing import Optional
from ..config import settings
from .groq_service import groq_service

class AudioService:
    def __init__(self):
        self.default_voice = settings.DEFAULT_TTS_VOICE

    async def generate_speech_base64(self, text: str, voice: Optional[str] = None) -> Optional[str]:
        """Generates TTS audio using edge-tts and returns it as a base64 encoded string."""
        voice_to_use = voice or self.default_voice
        try:
            import edge_tts
            communicate = edge_tts.Communicate(text, voice_to_use)
            audio_stream = io.BytesIO()
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_stream.write(chunk["data"])
            
            audio_bytes = audio_stream.getvalue()
            if audio_bytes:
                return base64.b64encode(audio_bytes).decode("utf-8")
        except Exception as e:
            print(f"[AudioService] edge-tts error: {e}. Note: TTS requires internet access or local fallback.")
        return None

    async def transcribe_audio(self, audio_bytes: bytes, filename: str = "audio.wav") -> str:
        """Transcribes incoming audio file via Groq Whisper."""
        return await groq_service.transcribe_audio(audio_bytes, filename)

audio_service = AudioService()
