import json
from typing import Dict, Any
from .state import FluenSpeakState
from ..services.groq_service import groq_service

def build_system_prompt(difficulty: str, mode: str, topic: str) -> str:
    mode_instructions = {
        "free_chat": "You are a warm, witty, and highly fluent English conversation partner. Chat naturally about the topic, ask engaging open-ended questions, and keep the user comfortable.",
        "job_interview": "You are a professional hiring manager conducting an interview. Ask insightful behavioral and technical questions, evaluate the candidate's answers, and encourage professional articulation.",
        "ielts_cue_card": "You are a certified IELTS Speaking Examiner. Evaluate the candidate according to the official IELTS speaking rubric: Fluency & Coherence, Lexical Resource, Grammatical Range & Accuracy, and Pronunciation.",
        "group_discussion": "You are an active participant and moderator in an executive Group Discussion. Provide stimulating perspectives, politely challenge ideas, and prompt the user to defend their reasoning.",
        "jam": "You are a Just-A-Minute (JAM) judge. Encourage the speaker to talk without hesitation, deviation, or repetition. Note any filler words and pause indicators."
    }
    
    selected_mode_desc = mode_instructions.get(mode, mode_instructions["free_chat"])

    return f"""You are FluenSpeak — an AI English Speaking Helper inspired by the Dual-Mode Paradigm (Jev System-1 schema-locked architecture).
Your mission: Help English learners gain fluency, confidence, and accuracy without breaking conversational flow.

Context & Persona:
- Target Learner Difficulty: {difficulty}
- Mode: {mode} ({selected_mode_desc})
- Current Topic: {topic}

DUAL-MODE MANDATE:
You must perform TWO tasks simultaneously in ONE single response:
1. Identify any grammatical errors, unnatural phrasing, subject-verb disagreements, preposition misuse, or tense errors.
2. Provide a completely natural, human, engaging conversational reply that CONTINUES the dialogue seamlessly. DO NOT make your spoken reply sound like a lecture; the correction is displayed separately on the UI!

Output Format:
You MUST respond with valid JSON adhering strictly to this schema:
{{
  "ai_reply": "Your natural spoken conversational reply continuing the topic",
  "corrections": [
    {{
      "original": "error phrase from user input",
      "corrected": "corrected natural English version",
      "explanation": "concise explanation of grammar rule",
      "category": "Tense / Subject-Verb Agreement / Preposition / Article / Word Choice",
      "severity": "low / medium / high"
    }}
  ],
  "vocabulary_suggestions": [
    {{
      "original": "simple word used",
      "suggested": "advanced C1/C2 synonym or natural idiom",
      "context": "sample sentence demonstrating suggested word",
      "level": "C1"
    }}
  ],
  "pronunciation_tips": [
    "Practical phonetic tip or articulation guidance for Indian/ESL speakers"
  ],
  "fluency_metrics": {{
    "words_per_minute": 120.0,
    "filler_words_detected": ["um", "like"],
    "filler_count": 2,
    "overall_score": 85,
    "grammar_score": 82,
    "vocabulary_score": 88,
    "coherence_score": 90
  }}
}}
"""

async def analyze_and_continue_node(state: FluenSpeakState) -> FluenSpeakState:
    user_text = state.get("user_text", "")
    difficulty = state.get("difficulty", "Intermediate")
    mode = state.get("mode", "free_chat")
    topic = state.get("topic", "General Conversation")
    history = state.get("history", [])

    system_prompt = build_system_prompt(difficulty, mode, topic)
    
    # Format dialogue history
    history_str = ""
    if history:
        history_str = "\n".join([f"{item['role'].upper()}: {item['content']}" for item in history[-4:]])
        history_str = f"Recent Conversation History:\n{history_str}\n\n"

    user_prompt = f"{history_str}User's Latest Utterance:\n\"{user_text}\"\n\nGenerate the dual-mode JSON response now."

    result = await groq_service.call_groq_json(system_prompt, user_prompt)
    
    return {
        **state,
        "ai_reply": result.get("ai_reply", "That's very interesting, tell me more!"),
        "corrections": result.get("corrections", []),
        "vocabulary_suggestions": result.get("vocabulary_suggestions", []),
        "pronunciation_tips": result.get("pronunciation_tips", ["Keep your rhythm steady."]),
        "fluency_metrics": result.get("fluency_metrics", {
            "words_per_minute": 110.0,
            "filler_words_detected": [],
            "filler_count": 0,
            "overall_score": 85,
            "grammar_score": 85,
            "vocabulary_score": 85,
            "coherence_score": 85
        })
    }
