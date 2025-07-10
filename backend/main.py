from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import random
from schema import ReflectionInput, EmotionResponse
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def analyze_emotion(text: str) -> EmotionResponse:
    text_lower = text.lower()

    if any(word in text_lower for word in ["nervous", "anxious", "worried", "scared"]):
        return EmotionResponse(emotion="Anxious", confidence=round(random.uniform(0.75, 0.95), 2))
    elif any(word in text_lower for word in ["happy", "excited", "joy", "great", "amazing"]):
        return EmotionResponse(emotion="Happy", confidence=round(random.uniform(0.80, 0.98), 2))
    elif any(word in text_lower for word in ["sad", "depressed", "down", "upset", "disappointed"]):
        return EmotionResponse(emotion="Sad", confidence=round(random.uniform(0.70, 0.90), 2))
    elif any(word in text_lower for word in ["angry", "mad", "furious", "annoyed", "frustrated"]):
        return EmotionResponse(emotion="Angry", confidence=round(random.uniform(0.65, 0.85), 2))
    elif any(word in text_lower for word in ["calm", "peaceful", "relaxed", "content"]):
        return EmotionResponse(emotion="Calm", confidence=round(random.uniform(0.75, 0.95), 2))
    else:
        return EmotionResponse(emotion="Neutral", confidence=round(random.uniform(0.60, 0.80), 2))

@app.get("/")
async def root():
    return {"message": "Emotion Reflection API"}

@app.post("/analyze", response_model=EmotionResponse)
async def analyze_reflection(reflection: ReflectionInput):
    if not reflection.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    result = analyze_emotion(reflection.text)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 