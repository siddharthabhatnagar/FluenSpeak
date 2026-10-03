# FluenSpeak AI Backend (Groq + LangChain + LangGraph + FastAPI)

FluenSpeak is an AI English Speaking Skill Enhancer based on the **Dual-Mode Paradigm** (inspired by Jev System-1 schema-locked inference). It simultaneously performs live grammar error detection and natural conversation continuation in a single fast forward pass.

## 🚀 Architecture Highlights

- **Framework**: FastAPI (Async, High-Throughput REST endpoints)
- **Agent Orchestration**: LangChain & LangGraph (`StateGraph` with Schema-Locked State)
- **LLM Engine**: Groq LPU with `llama-3.3-70b-versatile` / `llama-3.1-8b-instant` (~500 tokens/sec, <1.5s latency)
- **STT (Speech-to-Text)**: Groq Whisper Large v3 (`whisper-large-v3`)
- **TTS (Text-to-Speech)**: Microsoft Edge Neural TTS / Base64 audio streaming
- **Linguistic Engine**: Custom Indian English / ESL error classifier (Tenses, Subject-Verb Agreement, Introductions, Prepositions, Articles, Vocabulary Upgrades)
- **Resilient Fallback**: Offline ESL pattern matching engine for local development without API keys

---

## 📂 Project Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI application, CORS, routers
│   ├── config.py               # Settings (pydantic-settings / env vars)
│   ├── models/
│   │   └── schemas.py          # Request & response contracts
│   ├── graph/
│   │   ├── state.py            # LangGraph FluenSpeakState
│   │   ├── nodes.py            # LangGraph nodes (analysis & continuation)
│   │   └── workflow.py         # StateGraph compiled workflow
│   ├── services/
│   │   ├── groq_service.py     # Groq client & smart ESL fallback
│   │   ├── audio_service.py    # Edge-TTS & Whisper transcription
│   │   ├── exam_service.py     # IELTS Cue Cards, Job Interviews, GD, JAM
│   │   └── analytics_service.py# Error tracker, stats & drill generator
│   └── routers/
│       ├── chat.py             # POST /api/chat/dual-mode
│       ├── audio.py            # POST /api/audio/transcribe & /api/audio/tts
│       ├── exam.py             # GET /api/exam/prompts & POST /api/exam/evaluate
│       ├── analytics.py        # GET /api/analytics/summary
│       └── drills.py           # GET /api/drills/questions & POST /api/drills/verify
├── requirements.txt            # Python dependencies
├── .env.example                # Sample environment variables
├── .env                        # Local environment configuration
├── run.py                      # Local server runner
├── test_api.py                 # Automated backend test suite
├── Dockerfile                  # Container definition
├── render.yaml                 # Render Blueprint configuration
├── Procfile                    # Render / Railway / Heroku process runner
└── vercel.json                 # Vercel Serverless configuration
```

---

## ⚡ Deployment Options

### 1. Deploy on Render (Recommended)
1. Push this repository to GitHub.
2. Log in to [Render](https://render.com) and click **New > Blueprint**.
3. Select your repository. Render will automatically detect `render.yaml`.
4. In the Environment Variables, set:
   - `GROQ_API_KEY`: Your free Groq API key from [https://console.groq.com](https://console.groq.com)
5. Click **Apply**. Your backend will be live with free SSL!

### 2. Deploy on Vercel
1. Install Vercel CLI: `npm i -g vercel` or import via [vercel.com](https://vercel.com).
2. Run `vercel` inside the `backend/` folder.
3. Configure `GROQ_API_KEY` in Vercel Project Settings > Environment Variables.

### 3. Local Execution
```bash
cd backend
pip install -r requirements.txt
python run.py
```
Open interactive Swagger API docs at: `http://localhost:8000/docs`

---

## 🧪 Testing the API
Run the built-in test suite:
```bash
python test_api.py
```
All endpoints will be tested, verifying health, dual-mode analysis, exam prompts, analytics summary, and weakness drill generation.
