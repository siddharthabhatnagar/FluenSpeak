from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..services.audio_service import audio_service

router = APIRouter(prefix="/api/audio", tags=["Audio & Speech"])

class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = None

class TTSResponse(BaseModel):
    audio_base64: str
    format: str = "audio/mp3"

class TranscribeResponse(BaseModel):
    text: str

@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_audio_endpoint(file: UploadFile = File(...)):
    """Transcribes user voice input into text using Groq Whisper Large v3."""
    try:
        audio_bytes = await file.read()
        transcribed_text = await audio_service.transcribe_audio(audio_bytes, file.filename or "recording.wav")
        return TranscribeResponse(text=transcribed_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio transcription failed: {str(e)}")

@router.post("/tts", response_model=TTSResponse)
async def text_to_speech_endpoint(request: TTSRequest):
    """Generates natural neural voice audio from text."""
    try:
        audio_b64 = await audio_service.generate_speech_base64(request.text, request.voice)
        if not audio_b64:
            raise HTTPException(status_code=500, detail="Failed to synthesize speech audio.")
        return TTSResponse(audio_base64=audio_b64)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS error: {str(e)}")
