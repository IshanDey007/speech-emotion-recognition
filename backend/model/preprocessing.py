"""
Audio Preprocessing Module
Handles audio loading, feature extraction, and data augmentation
"""

import librosa
import numpy as np
import soundfile as sf
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class AudioPreprocessor:
    """Audio preprocessing and feature extraction"""
    
    def __init__(
        self,
        sample_rate: int = 22050,
        duration: float = 3.0,
        n_mfcc: int = 40,
        n_mels: int = 128
    ):
        """
        Initialize preprocessor
        
        Args:
            sample_rate: Target sample rate for audio
            duration: Target duration in seconds
            n_mfcc: Number of MFCC coefficients
            n_mels: Number of mel bands
        """
        self.sample_rate = sample_rate
        self.duration = duration
        self.n_mfcc = n_mfcc
        self.n_mels = n_mels
        self.max_length = int(sample_rate * duration)
    
    def load_audio(self, file_path: str) -> np.ndarray:
        """
        Load and normalize audio file
        
        Args:
            file_path: Path to audio file
        
        Returns:
            Normalized audio array
        """
        try:
            # Load audio
            audio, sr = librosa.load(file_path, sr=self.sample_rate, duration=self.duration)
            
            # Pad or trim to fixed length
            if len(audio) < self.max_length:
                audio = np.pad(audio, (0, self.max_length - len(audio)), mode='constant')
            else:
                audio = audio[:self.max_length]
            
            # Normalize
            audio = audio / (np.max(np.abs(audio)) + 1e-6)
            
            return audio
        
        except Exception as e:
            logger.error(f"Error loading audio {file_path}: {str(e)}")
            raise
    
    def extract_mfcc(self, audio: np.ndarray) -> np.ndarray:
        """
        Extract MFCC features
        
        Args:
            audio: Audio array
        
        Returns:
            MFCC features (n_mfcc, time_steps)
        """
        mfcc = librosa.feature.mfcc(
            y=audio,
            sr=self.sample_rate,
            n_mfcc=self.n_mfcc
        )
        
        # Normalize
        mfcc = (mfcc - np.mean(mfcc)) / (np.std(mfcc) + 1e-6)
        
        return mfcc
    
    def extract_mel_spectrogram(self, audio: np.ndarray) -> np.ndarray:
        """
        Extract mel spectrogram
        
        Args:
            audio: Audio array
        
        Returns:
            Mel spectrogram (n_mels, time_steps)
        """
        mel_spec = librosa.feature.melspectrogram(
            y=audio,
            sr=self.sample_rate,
            n_mels=self.n_mels
        )
        
        # Convert to log scale
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        
        # Normalize
        mel_spec_db = (mel_spec_db - np.mean(mel_spec_db)) / (np.std(mel_spec_db) + 1e-6)
        
        return mel_spec_db
    
    def extract_features(self, file_path: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Extract both MFCC and mel spectrogram features
        
        Args:
            file_path: Path to audio file
        
        Returns:
            Tuple of (mfcc, mel_spectrogram)
        """
        audio = self.load_audio(file_path)
        mfcc = self.extract_mfcc(audio)
        mel_spec = self.extract_mel_spectrogram(audio)
        
        return mfcc, mel_spec
    
    def augment_audio(self, audio: np.ndarray, augmentation_type: str = 'noise') -> np.ndarray:
        """
        Apply data augmentation to audio
        
        Args:
            audio: Audio array
            augmentation_type: Type of augmentation ('noise', 'pitch', 'speed')
        
        Returns:
            Augmented audio
        """
        if augmentation_type == 'noise':
            # Add white noise
            noise = np.random.randn(len(audio))
            audio_noise = audio + 0.005 * noise
            return audio_noise / (np.max(np.abs(audio_noise)) + 1e-6)
        
        elif augmentation_type == 'pitch':
            # Pitch shifting
            return librosa.effects.pitch_shift(audio, sr=self.sample_rate, n_steps=2)
        
        elif augmentation_type == 'speed':
            # Time stretching
            return librosa.effects.time_stretch(audio, rate=1.1)
        
        return audio
    
    def extract_additional_features(self, audio: np.ndarray) -> dict:
        """
        Extract additional audio features for analysis
        
        Args:
            audio: Audio array
        
        Returns:
            Dictionary of additional features
        """
        features = {}
        
        # Zero crossing rate
        features['zcr'] = np.mean(librosa.feature.zero_crossing_rate(audio))
        
        # Spectral centroid
        features['spectral_centroid'] = np.mean(
            librosa.feature.spectral_centroid(y=audio, sr=self.sample_rate)
        )
        
        # Spectral rolloff
        features['spectral_rolloff'] = np.mean(
            librosa.feature.spectral_rolloff(y=audio, sr=self.sample_rate)
        )
        
        # Chroma features
        features['chroma'] = np.mean(
            librosa.feature.chroma_stft(y=audio, sr=self.sample_rate)
        )
        
        # RMS energy
        features['rms'] = np.mean(librosa.feature.rms(y=audio))
        
        return features