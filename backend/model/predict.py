"""
Emotion Prediction Module
Handles inference using trained model
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
import pickle
import logging
from typing import Tuple, Dict
import os

from preprocessing import AudioPreprocessor

logger = logging.getLogger(__name__)

class EmotionPredictor:
    """Emotion prediction from audio files"""
    
    def __init__(self, model_path: str = 'saved_models/emotion_model.keras'):
        """
        Initialize predictor
        
        Args:
            model_path: Path to trained model
        """
        self.model_path = model_path
        self.label_encoder_path = 'saved_models/label_encoder.pkl'
        self.preprocessor = AudioPreprocessor()
        self.model = None
        self.label_encoder = None
        
        self.load_model()
    
    def load_model(self):
        """Load trained model and label encoder"""
        try:
            if os.path.exists(self.model_path):
                logger.info(f"Loading model from {self.model_path}")
                self.model = keras.models.load_model(self.model_path)
                logger.info("Model loaded successfully")
            else:
                logger.warning(f"Model not found at {self.model_path}")
                return
            
            if os.path.exists(self.label_encoder_path):
                with open(self.label_encoder_path, 'rb') as f:
                    self.label_encoder = pickle.load(f)
                logger.info("Label encoder loaded successfully")
            else:
                logger.warning(f"Label encoder not found at {self.label_encoder_path}")
        
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def predict(self, audio_path: str) -> Tuple[str, float, Dict[str, float]]:
        """
        Predict emotion from audio file
        
        Args:
            audio_path: Path to audio file
        
        Returns:
            Tuple of (emotion, confidence, probabilities_dict)
        """
        if self.model is None or self.label_encoder is None:
            raise ValueError("Model or label encoder not loaded")
        
        try:
            # Extract features
            mfcc, mel_spec = self.preprocessor.extract_features(audio_path)
            
            # Combine features
            combined_features = np.concatenate([mfcc, mel_spec], axis=0)
            features = combined_features.T  # (time_steps, features)
            
            # Add batch dimension
            features = np.expand_dims(features, axis=0)
            
            # Predict
            predictions = self.model.predict(features, verbose=0)[0]
            
            # Get predicted class
            predicted_idx = np.argmax(predictions)
            emotion = self.label_encoder.inverse_transform([predicted_idx])[0]
            confidence = float(predictions[predicted_idx])
            
            # Create probabilities dictionary
            probabilities = {
                self.label_encoder.inverse_transform([i])[0]: float(predictions[i])
                for i in range(len(predictions))
            }
            
            logger.info(f"Predicted emotion: {emotion} (confidence: {confidence:.4f})")
            
            return emotion, confidence, probabilities
        
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise
    
    def predict_batch(self, audio_paths: list) -> list:
        """
        Predict emotions for multiple audio files
        
        Args:
            audio_paths: List of audio file paths
        
        Returns:
            List of (emotion, confidence, probabilities) tuples
        """
        results = []
        for audio_path in audio_paths:
            try:
                result = self.predict(audio_path)
                results.append(result)
            except Exception as e:
                logger.error(f"Error predicting {audio_path}: {str(e)}")
                results.append((None, 0.0, {}))
        
        return results
    
    def get_emotion_statistics(self, predictions: list) -> Dict:
        """
        Calculate statistics from multiple predictions
        
        Args:
            predictions: List of prediction results
        
        Returns:
            Dictionary with emotion statistics
        """
        emotions = [pred[0] for pred in predictions if pred[0] is not None]
        
        if not emotions:
            return {}
        
        # Count emotions
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Calculate percentages
        total = len(emotions)
        emotion_percentages = {
            emotion: (count / total) * 100
            for emotion, count in emotion_counts.items()
        }
        
        # Most common emotion
        most_common = max(emotion_counts.items(), key=lambda x: x[1])
        
        return {
            'total_predictions': total,
            'emotion_counts': emotion_counts,
            'emotion_percentages': emotion_percentages,
            'most_common_emotion': most_common[0],
            'most_common_count': most_common[1]
        }