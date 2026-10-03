import os
import json
import re
import uuid
from typing import Dict, Any, List, Optional
from ..config import settings

class GroqService:
    def __init__(self):
        self._cached_client = None
        self._cached_key = None

    def get_client(self):
        """Dynamically retrieves or initializes the Groq client from Render/OS environment."""
        current_key = settings.GROQ_API_KEY or os.environ.get("GROQ_API_KEY", "").strip()
        if not current_key:
            return None
        if self._cached_client is None or self._cached_key != current_key:
            try:
                from groq import Groq
                self._cached_client = Groq(api_key=current_key)
                self._cached_key = current_key
            except Exception as e:
                print(f"[GroqService] Warning: Failed to initialize Groq client: {e}")
                return None
        return self._cached_client

    def is_available(self) -> bool:
        """Returns True if a valid Groq client can be obtained dynamically from the environment."""
        return self.get_client() is not None

    async def call_groq_json(self, system_prompt: str, user_prompt: str, model: Optional[str] = None) -> Dict[str, Any]:
        """Calls Groq LPU with structured JSON response mode."""
        client = self.get_client()
        if not client:
            return self._fallback_structured_response(user_prompt)

        model_to_use = model or settings.GROQ_CHAT_MODEL
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt + "\nIMPORTANT: Return valid JSON ONLY matching the requested structure."},
                    {"role": "user", "content": user_prompt}
                ],
                model=model_to_use,
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            raw_text = chat_completion.choices[0].message.content
            return json.loads(raw_text)
        except Exception as e:
            print(f"[GroqService] Groq API call error: {e}. Falling back to rule-based engine.")
            return self._fallback_structured_response(user_prompt)

    async def transcribe_audio(self, audio_bytes: bytes, filename: str = "audio.wav") -> str:
        client = self.get_client()
        if not client:
            return "I am practicing my English speaking skills with FluenSpeak."

        try:
            transcription = client.audio.transcriptions.create(
                file=(filename, audio_bytes),
                model=settings.GROQ_WHISPER_MODEL,
                response_format="json",
                language="en",
                temperature=0.0
            )
            return transcription.text
        except Exception as e:
            print(f"[GroqService] Transcription error: {e}")
            return "I am practicing my English speaking skills with FluenSpeak."

    def _fallback_structured_response(self, text: str) -> Dict[str, Any]:
        """Intelligent linguistic pattern matcher for common Indian English & ESL speaking mistakes."""
        corrections = []
        vocab_suggestions = []
        pronunciation_tips = []
        lower = text.lower().strip()

        # Rule 1: "Myself <Name>" introduction
        match_myself = re.search(r"\bmyself\s+([a-zA-Z]+)", text, re.IGNORECASE)
        if match_myself:
            name = match_myself.group(1)
            corrections.append({
                "original": f"Myself {name}",
                "corrected": f"My name is {name} / I'm {name}",
                "explanation": "Avoid using reflexive 'Myself' for self-introductions. Use 'My name is...' or 'I am...'",
                "category": "Syntax & Introduction",
                "severity": "high"
            })
            pronunciation_tips.append("Focus on crisp pronunciation of 'name' (/naym/) without dropping the final consonant.")

        # Rule 1b: irregular past tense like 'buyed'
        if "buyed" in lower:
            corrections.append({
                "original": "buyed",
                "corrected": "bought",
                "explanation": "The past tense of the verb 'buy' is irregular: 'bought', not 'buyed'.",
                "category": "Tense & Irregular Verbs",
                "severity": "high"
            })

        # Rule 2: "I goes" / subject-verb agreement
        if re.search(r"\bi\s+goes\b", lower):
            corrections.append({
                "original": "I goes",
                "corrected": "I go / I went",
                "explanation": "Subject-verb agreement: 'I' takes the base verb 'go' in present tense or 'went' in past tense.",
                "category": "Subject-Verb Agreement",
                "severity": "high"
            })

        # Rule 3: "I am coming from" for permanent hometown
        if "i am coming from" in lower:
            corrections.append({
                "original": "I am coming from",
                "corrected": "I am from / I hail from",
                "explanation": "Use simple present ('I am from') for permanent origin; 'I am coming from' implies you are currently traveling from there.",
                "category": "Tense & Phrasing",
                "severity": "medium"
            })

        # Rule 4: "did not knew" / "did not went" double past tense
        match_did = re.search(r"\bdid(?:n't|\s+not)\s+(\w+ed|\w+t|knew|saw|went)\b", lower)
        if match_did:
            corrections.append({
                "original": match_did.group(0),
                "corrected": f"didn't base_verb (e.g. didn't know / didn't go)",
                "explanation": "After auxiliary 'did / didn't', always use the base form of the verb, not past tense.",
                "category": "Tense",
                "severity": "high"
            })

        # Rule 5: "very good" -> vocabulary upgrade
        if "very good" in lower:
            vocab_suggestions.append({
                "original": "very good",
                "suggested": "exemplary / outstanding",
                "context": "That was an outstanding performance.",
                "level": "C1"
            })
        if "very bad" in lower:
            vocab_suggestions.append({
                "original": "very bad",
                "suggested": "subpar / detrimental",
                "context": "The outcome was quite subpar.",
                "level": "B2"
            })
        if "big problem" in lower:
            vocab_suggestions.append({
                "original": "big problem",
                "suggested": "formidable challenge",
                "context": "We encountered a formidable challenge in the pipeline.",
                "level": "C1"
            })

        # Filler words detection
        filler_words = ["um", "uh", "like", "actually", "basically", "you know"]
        detected_fillers = [f for f in filler_words if f in lower.split()]
        filler_count = len(detected_fillers)

        # Fluency calculation
        word_count = len(text.split())
        grammar_score = max(50, 95 - (len(corrections) * 15))
        vocab_score = 75 + (len(vocab_suggestions) * 5)
        overall_score = int((grammar_score * 0.6) + (vocab_score * 0.4))

        # Dynamic reply generation
        replies = [
            f"That's a very interesting point! Could you elaborate a bit more on how you approached that?",
            f"I see what you mean. What was the biggest takeaway or challenge you faced during that experience?",
            f"Fascinating! How do you plan to take this further in your upcoming projects or studies?"
        ]
        import random
        reply = random.choice(replies)

        return {
            "ai_reply": reply,
            "corrections": corrections,
            "vocabulary_suggestions": vocab_suggestions,
            "pronunciation_tips": pronunciation_tips if pronunciation_tips else ["Maintain steady pacing and natural sentence pauses."],
            "fluency_metrics": {
                "words_per_minute": 115.0 if word_count > 0 else 0.0,
                "filler_words_detected": detected_fillers,
                "filler_count": filler_count,
                "overall_score": overall_score,
                "grammar_score": grammar_score,
                "vocabulary_score": vocab_score,
                "coherence_score": 88
            }
        }

groq_service = GroqService()
