from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from schema import ReflectionInput, EmotionResponse
from emotion_service import emotion_analyzer
from validators import validate_reflection_text
from exceptions import handle_analysis_error, EmotionAnalysisError

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(EmotionAnalysisError)
async def emotion_analysis_exception_handler(request: Request, exc: EmotionAnalysisError):
    http_exception = handle_analysis_error(exc)
    return JSONResponse(
        status_code=http_exception.status_code,
        content=http_exception.detail
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred"
        }
    )

@app.post("/analyze", response_model=EmotionResponse)
async def analyze_reflection(reflection: ReflectionInput) -> EmotionResponse:
    try:
        validated_text = validate_reflection_text(reflection.text)
        result = emotion_analyzer.analyze_emotion(validated_text)
        return result
        
    except EmotionAnalysisError as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during analysis"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 