from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import chat_router, audio_router, exam_router, analytics_router, drills_router
from .services.groq_service import groq_service

app = FastAPI(
    title="FluenSpeak AI Backend",
    description="Dual-Mode AI English Speaking Skill Enhancer powered by Groq, LangChain & LangGraph",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(chat_router)
app.include_router(audio_router)
app.include_router(exam_router)
app.include_router(analytics_router)
app.include_router(drills_router)

@app.get("/")
async def root():
    return {
        "app": "FluenSpeak AI Backend",
        "status": "online",
        "engine": "Groq + LangChain + LangGraph",
        "groq_connected": groq_service.is_available(),
        "model": settings.GROQ_CHAT_MODEL,
        "docs_url": "/docs"
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "groq_active": groq_service.is_available(),
        "whisper_model": settings.GROQ_WHISPER_MODEL
    }
