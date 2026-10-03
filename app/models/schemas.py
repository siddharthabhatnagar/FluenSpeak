from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class GrammarCorrection(BaseModel):
    original: str = Field(..., description="Original erroneous word or phrase")
    corrected: str = Field(..., description="Corrected phrasing")
    explanation: str = Field(..., description="Linguistic explanation of the rule")
    category: str = Field("Grammar", description="Category: Tense, Subject-Verb Agreement, Preposition, Article, Word Choice, etc.")
    severity: str = Field("medium", description="Severity: low, medium, high")

class VocabularySuggestion(BaseModel):
    original: str = Field(..., description="Original simple word")
    suggested: str = Field(..., description="Sophisticated or natural synonym")
    context: str = Field("", description="How to use it in a sentence")
    level: str = Field("B2/C1", description="CEFR or IELTS level")

class FluencyMetrics(BaseModel):
    words_per_minute: float = 0.0
    filler_words_detected: List[str] = Field(default_factory=list)
    filler_count: int = 0
    overall_score: int = Field(85, ge=0, le=100)
    grammar_score: int = Field(80, ge=0, le=100)
    vocabulary_score: int = Field(80, ge=0, le=100)
    coherence_score: int = Field(85, ge=0, le=100)

class MessageItem(BaseModel):
    role: str # "user" or "assistant"
    content: str

class DualModeRequest(BaseModel):
    user_text: str
    difficulty: str = "Intermediate" # Beginner, Intermediate, Advanced, IELTS Band 7+
    mode: str = "free_chat" # free_chat, job_interview, ielts_cue_card, group_discussion, jam
    topic: Optional[str] = "General Conversation"
    history: List[MessageItem] = Field(default_factory=list)
    voice_enabled: bool = False

class DualModeResponse(BaseModel):
    id: str
    user_text: str
    ai_reply: str
    corrections: List[GrammarCorrection] = Field(default_factory=list)
    vocabulary_suggestions: List[VocabularySuggestion] = Field(default_factory=list)
    pronunciation_tips: List[str] = Field(default_factory=list)
    fluency_metrics: FluencyMetrics = Field(default_factory=FluencyMetrics)
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    audio_base64: Optional[str] = None

class ExamEvaluationRequest(BaseModel):
    exam_type: str # ielts, job_interview, gd, jam
    topic: str
    transcript: str
    time_taken_seconds: int = 60

class ExamRubricScore(BaseModel):
    band_score: float # e.g. 7.5
    fluency_and_coherence: float
    lexical_resource: float
    grammatical_accuracy: float
    pronunciation_and_clarity: float
    strengths: List[str]
    areas_for_improvement: List[str]
    model_answer_excerpt: str
    corrections: List[GrammarCorrection] = Field(default_factory=list)

class DrillQuestion(BaseModel):
    id: str
    question: str
    options: List[str]
    correct_option_index: int
    rule_category: str
    explanation: str

class DrillEvaluationRequest(BaseModel):
    question_id: str
    selected_option_index: int
    rule_category: str

class AnalyticsSummary(BaseModel):
    total_sessions: int
    total_minutes_spoken: float
    average_fluency_score: float
    common_mistakes_by_category: Dict[str, int]
    weekly_progress: List[Dict[str, Any]]
    streak_days: int
    current_level: str
