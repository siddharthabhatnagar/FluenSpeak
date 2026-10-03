from typing import List, Dict, Any
from ..models.schemas import ExamRubricScore, GrammarCorrection
from .groq_service import groq_service

CUE_CARDS = [
    {
        "id": "ielts_1",
        "title": "Describe a difficult decision you had to make",
        "category": "IELTS Cue Card (Part 2)",
        "prep_time_seconds": 60,
        "speak_time_seconds": 120,
        "bullets": [
            "What the decision was",
            "When and why you had to make it",
            "What alternative choices you considered",
            "Explain how you felt after making the decision and what the result was"
        ]
    },
    {
        "id": "ielts_2",
        "title": "Describe a person who has greatly influenced your life",
        "category": "IELTS Cue Card (Part 2)",
        "prep_time_seconds": 60,
        "speak_time_seconds": 120,
        "bullets": [
            "Who this person is and how you know them",
            "What qualities make them special or inspiring",
            "What lessons or values they taught you",
            "Explain why they have had such a lasting impact on you"
        ]
    },
    {
        "id": "job_1",
        "title": "Tell me about yourself and your professional journey",
        "category": "Job Interview (HR / Tech)",
        "prep_time_seconds": 30,
        "speak_time_seconds": 90,
        "bullets": [
            "Your educational background and technical interests",
            "Key projects or milestones you have achieved",
            "Your professional strengths and passions",
            "Why you are excited about this role"
        ]
    },
    {
        "id": "gd_1",
        "title": "Artificial Intelligence: Catalyst for Innovation or Threat to Jobs?",
        "category": "Group Discussion (GD)",
        "prep_time_seconds": 45,
        "speak_time_seconds": 90,
        "bullets": [
            "State your core thesis clearly",
            "Provide concrete examples of industry transformation",
            "Acknowledge the counter-argument (job displacement vs job creation)",
            "Conclude with a balanced recommendation for upskilling"
        ]
    },
    {
        "id": "jam_1",
        "title": "The Role of Failure in Achieving Success",
        "category": "Just-A-Minute (JAM)",
        "prep_time_seconds": 15,
        "speak_time_seconds": 60,
        "bullets": [
            "Speak continuously for 60 seconds",
            "Zero hesitation, zero stuttering, zero repetition",
            "Maintain strong voice modulation and compelling narrative"
        ]
    }
]

class ExamService:
    def get_all_prompts(self) -> List[Dict[str, Any]]:
        return CUE_CARDS

    async def evaluate_exam(self, exam_type: str, topic: str, transcript: str, time_taken: int) -> ExamRubricScore:
        system_prompt = """You are a master IELTS Speaking Examiner and Senior Corporate Interview Evaluator.
Evaluate the candidate's spoken transcript rigorously according to standard rubric criteria.
Output valid JSON adhering to:
{
  "band_score": 7.5,
  "fluency_and_coherence": 7.5,
  "lexical_resource": 7.0,
  "grammatical_accuracy": 7.5,
  "pronunciation_and_clarity": 8.0,
  "strengths": ["Clear structure", "Good pacing"],
  "areas_for_improvement": ["Use more varied transitional phrases", "Eliminate occasional filler words"],
  "model_answer_excerpt": "An advanced, natural way to express the core idea...",
  "corrections": [
    {
      "original": "phrase with error",
      "corrected": "better version",
      "explanation": "rule explanation",
      "category": "Grammar / Lexicon",
      "severity": "medium"
    }
  ]
}"""
        user_prompt = f"Exam Type: {exam_type}\nTopic: {topic}\nTime Spoken: {time_taken}s\nCandidate Transcript:\n\"{transcript}\""
        
        result = await groq_service.call_groq_json(system_prompt, user_prompt)
        
        corrections = [
            GrammarCorrection(**c) if isinstance(c, dict) else c
            for c in result.get("corrections", [])
        ]
        
        return ExamRubricScore(
            band_score=float(result.get("band_score", 7.0)),
            fluency_and_coherence=float(result.get("fluency_and_coherence", 7.0)),
            lexical_resource=float(result.get("lexical_resource", 7.0)),
            grammatical_accuracy=float(result.get("grammatical_accuracy", 7.0)),
            pronunciation_and_clarity=float(result.get("pronunciation_and_clarity", 7.5)),
            strengths=result.get("strengths", ["Maintained conversational flow", "Addresses topic directly"]),
            areas_for_improvement=result.get("areas_for_improvement", ["Expand vocabulary range", "Watch subject-verb agreement"]),
            model_answer_excerpt=result.get("model_answer_excerpt", "In tackling this challenge, I prioritized structured problem solving..."),
            corrections=corrections
        )

exam_service = ExamService()
