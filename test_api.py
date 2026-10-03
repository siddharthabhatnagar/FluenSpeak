import asyncio
import httpx
import json

async def test_backend():
    print("Testing FluenSpeak Backend Endpoints directly...")
    from app.main import app
    from httpx import ASGITransport, AsyncClient

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Health check
        res = await client.get("/")
        print("Root response:", res.status_code, res.json())
        assert res.status_code == 200

        # 2. Dual-mode chat
        payload = {
            "user_text": "Myself Rahul, I goes to market yesterday and buyed a very good phone.",
            "difficulty": "Intermediate",
            "mode": "job_interview",
            "topic": "Tell me about yourself"
        }
        res = await client.post("/api/chat/dual-mode", json=payload)
        print("\nDual-Mode Status:", res.status_code)
        data = res.json()
        print("AI Spoken Reply:", data.get("ai_reply"))
        print("Corrections Detected:", len(data.get("corrections", [])))
        for c in data.get("corrections", []):
            print(f" - [{c.get('category')}] '{c.get('original')}' -> '{c.get('corrected')}': {c.get('explanation')}")
        print("Vocabulary Suggestions:", data.get("vocabulary_suggestions"))
        print("Fluency Metrics:", data.get("fluency_metrics"))
        assert res.status_code == 200
        assert len(data.get("corrections", [])) > 0

        # 3. Exam prompts
        res = await client.get("/api/exam/prompts")
        print("\nExam Prompts count:", len(res.json()))
        assert res.status_code == 200

        # 4. Analytics
        res = await client.get("/api/analytics/summary")
        print("\nAnalytics Summary:", res.json().get("current_level"))
        assert res.status_code == 200

        # 5. Drills
        res = await client.get("/api/drills/questions")
        print("\nDrill questions count:", len(res.json()))
        assert res.status_code == 200
    print("\nALL BACKEND API TESTS PASSED SUCCESSFULLY! [OK]")

if __name__ == "__main__":
    asyncio.run(test_backend())
