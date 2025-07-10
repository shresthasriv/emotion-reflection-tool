from fastapi import HTTPException
from typing import Optional


class EmotionAnalysisError(Exception):
    def __init__(self, message: str, error_code: Optional[str] = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class InvalidInputError(EmotionAnalysisError):
    pass


class AnalysisProcessingError(EmotionAnalysisError):
    pass


class ServerError(EmotionAnalysisError):
    pass


def handle_analysis_error(error: Exception) -> HTTPException:
    if isinstance(error, InvalidInputError):
        return HTTPException(
            status_code=400,
            detail={
                "error": "Invalid Input",
                "message": error.message,
                "error_code": error.error_code or "INVALID_INPUT"
            }
        )
    elif isinstance(error, AnalysisProcessingError):
        return HTTPException(
            status_code=422,
            detail={
                "error": "Processing Failed",
                "message": error.message,
                "error_code": error.error_code or "ANALYSIS_FAILED"
            }
        )
    elif isinstance(error, ServerError):
        return HTTPException(
            status_code=500,
            detail={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred",
                "error_code": error.error_code or "INTERNAL_ERROR"
            }
        )
    else:
        return HTTPException(
            status_code=500,
            detail={
                "error": "Unknown Error",
                "message": "An unexpected error occurred",
                "error_code": "UNKNOWN_ERROR"
            }
        ) 