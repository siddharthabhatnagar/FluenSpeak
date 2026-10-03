from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict

class FluenSpeakState(TypedDict, total=False):
    # Inputs
    user_text: str
    difficulty: str
    mode: str
    topic: str
    history: List[Dict[str, str]]
    voice_enabled: bool
    
    # Internal agent scratchpad & intermediate decisions
    intent: str
    raw_analysis: Dict[str, Any]
    
    # Dual-Mode Outputs
    corrections: List[Dict[str, Any]]
    vocabulary_suggestions: List[Dict[str, Any]]
    pronunciation_tips: List[str]
    ai_reply: str
    fluency_metrics: Dict[str, Any]
    
    # Exam / Special mode evaluations
    exam_evaluation: Optional[Dict[str, Any]]
    error: Optional[str]
