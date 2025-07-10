import random
from typing import Dict, List, Tuple
from schema import EmotionResponse
from exceptions import AnalysisProcessingError, ServerError
from validators import validate_confidence_score


class EmotionAnalyzer:

    def __init__(self):
        self.emotion_keywords = {
            "anxious": ["nervous", "anxious", "worried", "scared", "afraid", "fearful", "concerned", "stressed"],
            "happy": ["happy", "excited", "joy", "great", "amazing", "wonderful", "fantastic", "thrilled", "delighted"],
            "sad": ["sad", "depressed", "down", "upset", "disappointed", "miserable", "gloomy", "heartbroken"],
            "angry": ["angry", "mad", "furious", "annoyed", "frustrated", "irritated", "outraged", "livid"],
            "calm": ["calm", "peaceful", "relaxed", "content", "serene", "tranquil", "composed", "zen"],
            "surprised": ["surprised", "shocked", "amazed", "astonished", "stunned", "bewildered"],
            "confused": ["confused", "puzzled", "perplexed", "uncertain", "lost", "unclear"]
        }
        
        self.confidence_ranges = {
            "anxious": (0.75, 0.95),
            "happy": (0.80, 0.98),
            "sad": (0.70, 0.90),
            "angry": (0.65, 0.85),
            "calm": (0.75, 0.95),
            "surprised": (0.70, 0.88),
            "confused": (0.60, 0.80)
        }
    
    def analyze_emotion(self, text: str) -> EmotionResponse:
        try:
            emotion, base_confidence = self._detect_emotion(text)
            confidence = self._calculate_confidence(emotion, base_confidence, text)
            validated_confidence = validate_confidence_score(confidence)
            
            result = EmotionResponse(emotion=emotion, confidence=validated_confidence)
            return result
            
        except Exception as e:
            if isinstance(e, (AnalysisProcessingError, ServerError)):
                raise
            else:
                raise ServerError(f"Unexpected error during analysis: {str(e)}", "ANALYSIS_ERROR")
    
    def _detect_emotion(self, text: str) -> Tuple[str, float]:
        try:
            text_lower = text.lower()
            emotion_scores = {}

            for emotion, keywords in self.emotion_keywords.items():
                score = sum(1 for keyword in keywords if keyword in text_lower)
                if score > 0:
                    emotion_scores[emotion] = score
            
            if not emotion_scores:
                return "Neutral", 0.65

            primary_emotion = max(emotion_scores, key=emotion_scores.get)
            base_confidence = min(0.95, 0.6 + (emotion_scores[primary_emotion] * 0.1))
            
            return primary_emotion.capitalize(), base_confidence
            
        except Exception as e:
            raise AnalysisProcessingError(f"Failed to detect emotion: {str(e)}", "DETECTION_FAILED")
    
    def _calculate_confidence(self, emotion: str, base_confidence: float, text: str) -> float:
        try:
            emotion_lower = emotion.lower()
            
            if emotion_lower in self.confidence_ranges:
                min_conf, max_conf = self.confidence_ranges[emotion_lower]
                random_factor = random.uniform(0.8, 1.2)
                adjusted_confidence = base_confidence * random_factor
                final_confidence = max(min_conf, min(max_conf, adjusted_confidence))
            else:
                final_confidence = random.uniform(0.60, 0.80)

            length_bonus = min(0.05, len(text) / 2000)
            final_confidence = min(0.99, final_confidence + length_bonus)
            
            return round(final_confidence, 2)
            
        except Exception as e:
            return 0.75


emotion_analyzer = EmotionAnalyzer() 