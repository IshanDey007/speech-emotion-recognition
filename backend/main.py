"""
Speech Emotion Recognition API
FastAPI backend for emotion detection from audio files
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Optional
import uvicorn
import os
import tempfile
import logging
from datetime import datetime

from model.predict import EmotionPredictor
from model.preprocessing import AudioPreprocessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Speech Emotion Recognition API",
    description="AI-powered emotion detection from speech for customer satisfaction analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model and preprocessor
predictor = None
preprocessor = AudioPreprocessor()

# Response models
class EmotionResponse(BaseModel):
    emotion: str
    confidence: float
    probabilities: Dict[str, float]
    satisfaction_score: float
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    version: str

class BatchEmotionResponse(BaseModel):
    results: List[EmotionResponse]
    average_satisfaction: float

# Emotion to satisfaction mapping
EMOTION_SATISFACTION_MAP = {
    "happiness": 9.0,
    "surprise": 7.0,
    "neutral": 6.0,
    "sadness": 3.0,
    "fear": 2.5,
    "disgust": 2.0,
    "anger": 1.0
}

def calculate_satisfaction_score(emotion: str, confidence: float) -> float:
    """Calculate satisfaction score based on emotion and confidence"""
    base_score = EMOTION_SATISFACTION_MAP.get(emotion, 5.0)
    # Adjust score based on confidence
    adjusted_score = base_score * confidence + 5.0 * (1 - confidence)
    return round(adjusted_score, 2)

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    global predictor
    try:
        logger.info("Loading emotion recognition model...")
        predictor = EmotionPredictor()
        logger.info("Model loaded successfully!")
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        logger.warning("API will start but predictions will fail until model is trained")

@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        model_loaded=predictor is not None and predictor.model is not None,
        version="1.0.0"
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check"""
    return HealthResponse(
        status="healthy" if predictor and predictor.model else "model_not_loaded",
        model_loaded=predictor is not None and predictor.model is not None,
        version="1.0.0"
    )

@app.post("/api/predict", response_model=EmotionResponse)
async def predict_emotion(file: UploadFile = File(...)):
    """
    Predict emotion from uploaded audio file
    
    Args:
        file: Audio file (WAV, MP3, FLAC supported)
    
    Returns:
        EmotionResponse with detected emotion and probabilities
    """
    if not predictor or not predictor.model:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please train the model first."
        )
    
    # Validate file type
    allowed_extensions = ['.wav', '.mp3', '.flac', '.ogg']
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Save uploaded file temporarily
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        # Predict emotion
        logger.info(f"Processing file: {file.filename}")
        emotion, confidence, probabilities = predictor.predict(tmp_path)
        
        # Calculate satisfaction score
        satisfaction_score = calculate_satisfaction_score(emotion, confidence)
        
        # Clean up
        os.unlink(tmp_path)
        
        return EmotionResponse(
            emotion=emotion,
            confidence=round(confidence, 4),
            probabilities={k: round(v, 4) for k, v in probabilities.items()},
            satisfaction_score=satisfaction_score,
            timestamp=datetime.utcnow().isoformat()
        )
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/api/predict/batch", response_model=BatchEmotionResponse)
async def predict_batch(files: List[UploadFile] = File(...)):
    """
    Predict emotions for multiple audio files
    
    Args:
        files: List of audio files
    
    Returns:
        BatchEmotionResponse with results for all files
    """
    if not predictor or not predictor.model:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please train the model first."
        )
    
    if len(files) > 10:
        raise HTTPException(
            status_code=400,
            detail="Maximum 10 files allowed per batch"
        )
    
    results = []
    satisfaction_scores = []
    
    for file in files:
        try:
            # Process each file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                content = await file.read()
                tmp_file.write(content)
                tmp_path = tmp_file.name
            
            emotion, confidence, probabilities = predictor.predict(tmp_path)
            satisfaction_score = calculate_satisfaction_score(emotion, confidence)
            
            results.append(EmotionResponse(
                emotion=emotion,
                confidence=round(confidence, 4),
                probabilities={k: round(v, 4) for k, v in probabilities.items()},
                satisfaction_score=satisfaction_score,
                timestamp=datetime.utcnow().isoformat()
            ))
            
            satisfaction_scores.append(satisfaction_score)
            os.unlink(tmp_path)
            
        except Exception as e:
            logger.error(f"Error processing {file.filename}: {str(e)}")
            continue
    
    avg_satisfaction = sum(satisfaction_scores) / len(satisfaction_scores) if satisfaction_scores else 0
    
    return BatchEmotionResponse(
        results=results,
        average_satisfaction=round(avg_satisfaction, 2)
    )

@app.get("/api/emotions")
async def get_emotions():
    """Get list of supported emotions"""
    return {
        "emotions": list(EMOTION_SATISFACTION_MAP.keys()),
        "count": len(EMOTION_SATISFACTION_MAP)
    }

@app.get("/api/stats")
async def get_stats():
    """Get API statistics"""
    return {
        "model_loaded": predictor is not None and predictor.model is not None,
        "supported_emotions": len(EMOTION_SATISFACTION_MAP),
        "max_batch_size": 10,
        "supported_formats": [".wav", ".mp3", ".flac", ".ogg"]
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )