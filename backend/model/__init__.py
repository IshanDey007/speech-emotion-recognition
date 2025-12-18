"""
Model package for Speech Emotion Recognition
"""

from .preprocessing import AudioPreprocessor
from .predict import EmotionPredictor
from .train_model import EmotionRecognitionModel

__all__ = ['AudioPreprocessor', 'EmotionPredictor', 'EmotionRecognitionModel']