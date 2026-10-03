import uuid
from fastapi import APIRouter, HTTPException
from ..models.schemas import DualModeRequest, DualModeResponse, GrammarCorrection, VocabularySuggestion, FluencyMetrics
from ..graph.workflow import fluenspeak_graph
from ..services.audio_service import audio_service
from ..services.analytics_service import analytics_service

router = APIRouter(prefix="/api/chat", tags=["Dual-Mode Chat"])

@router.post("/dual-mode", response_model=DualModeResponse)
async def process_dual_mode(request: DualModeRequest):
    """
    FluenSpeak Core Dual-Mode Endpoint:
    Simultaneously performs grammar error identification and natural conversation continuation
    in a single low-latency pass (Schema-Locked System-1 style via LangGraph + Groq LLaMA).
    """
    try:
        # Run state through LangGraph workflow
        initial_state = {
            "user_text": request.user_text,
            "difficulty": request.difficulty,
            "mode": request.mode,
            "topic": request.topic or "General Conversation",
            "history": [msg.model_dump() for msg in request.history],
            "voice_enabled": request.voice_enabled
        }
        
        final_state = await fluenspeak_graph.ainvoke(initial_state)

        # Parse corrections and vocabulary suggestions
        corrections = [
            GrammarCorrection(**c) if isinstance(c, dict) else c
            for c in final_state.get("corrections", [])
        ]
        
        vocab_suggestions = [
            VocabularySuggestion(**v) if isinstance(v, dict) else v
            for v in final_state.get("vocabulary_suggestions", [])
        ]
        
        fluency_metrics_dict = final_state.get("fluency_metrics", {})
        fluency_metrics = FluencyMetrics(**fluency_metrics_dict) if isinstance(fluency_metrics_dict, dict) else fluency_metrics_dict

        ai_reply = final_state.get("ai_reply", "That's very interesting, tell me more!")
        
        # Audio generation if voice enabled
        audio_base64 = None
        if request.voice_enabled:
            audio_base64 = await audio_service.generate_speech_base64(ai_reply)

        # Record metrics for user analytics profile
        word_count = len(request.user_text.split())
        analytics_service.record_turn([c.model_dump() for c in corrections], word_count)

        response_id = f"resp_{uuid.uuid4().hex[:10]}"

        return DualModeResponse(
            id=response_id,
            user_text=request.user_text,
            ai_reply=ai_reply,
            corrections=corrections,
            vocabulary_suggestions=vocab_suggestions,
            pronunciation_tips=final_state.get("pronunciation_tips", []),
            fluency_metrics=fluency_metrics,
            audio_base64=audio_base64
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"FluenSpeak processing error: {str(e)}")
