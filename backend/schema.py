from pydantic import BaseModel

class ReflectionInput(BaseModel):
    text: str

class EmotionResponse(BaseModel):
    emotion: str
    confidence: float
