import os
from typing import List

# Try to load local .env if present without overriding real OS environment variables
try:
    from dotenv import load_dotenv
    load_dotenv(override=False)
except ImportError:
    pass

class Settings:
    @property
    def GROQ_API_KEY(self) -> str:
        return os.environ.get("GROQ_API_KEY", "").strip()

    @property
    def GROQ_CHAT_MODEL(self) -> str:
        return os.environ.get("GROQ_CHAT_MODEL", "llama-3.3-70b-versatile").strip()

    @property
    def GROQ_FAST_MODEL(self) -> str:
        return os.environ.get("GROQ_FAST_MODEL", "llama-3.1-8b-instant").strip()

    @property
    def GROQ_WHISPER_MODEL(self) -> str:
        return os.environ.get("GROQ_WHISPER_MODEL", "whisper-large-v3").strip()

    @property
    def HOST(self) -> str:
        return os.environ.get("HOST", "0.0.0.0").strip()

    @property
    def PORT(self) -> int:
        # Render sets $PORT dynamically (e.g. 10000)
        return int(os.environ.get("PORT", "8000"))

    @property
    def ENVIRONMENT(self) -> str:
        return os.environ.get("ENVIRONMENT", "production" if os.environ.get("RENDER") else "development").strip()

    @property
    def DEFAULT_TTS_VOICE(self) -> str:
        return os.environ.get("DEFAULT_TTS_VOICE", "en-US-JennyNeural").strip()

    @property
    def CORS_ORIGINS(self) -> List[str]:
        custom_origins = os.environ.get("CORS_ORIGINS", "")
        if custom_origins:
            return [o.strip() for o in custom_origins.split(",") if o.strip()]
        return [
            "*",
            "http://localhost:8080",
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:8080",
        ]

settings = Settings()
