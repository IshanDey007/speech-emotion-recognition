"""
Model Training Script
Trains CNN-LSTM model on SAVEE dataset for emotion recognition
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle
import logging
from tqdm import tqdm
import json

from preprocessing import AudioPreprocessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmotionRecognitionModel:
    """CNN-LSTM model for speech emotion recognition"""
    
    def __init__(self, input_shape: tuple, num_classes: int):
        """
        Initialize model
        
        Args:
            input_shape: Shape of input features (time_steps, features)
            num_classes: Number of emotion classes
        """
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.model = None
        self.history = None
    
    def build_model(self) -> keras.Model:
        """
        Build CNN-LSTM architecture
        
        Returns:
            Compiled Keras model
        """
        model = models.Sequential([
            # Input layer
            layers.Input(shape=self.input_shape),
            
            # CNN layers for feature extraction
            layers.Conv1D(64, kernel_size=5, activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling1D(pool_size=2),
            layers.Dropout(0.3),
            
            layers.Conv1D(128, kernel_size=5, activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling1D(pool_size=2),
            layers.Dropout(0.3),
            
            layers.Conv1D(256, kernel_size=3, activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling1D(pool_size=2),
            layers.Dropout(0.3),
            
            # LSTM layers for temporal modeling
            layers.LSTM(128, return_sequences=True),
            layers.Dropout(0.3),
            
            layers.LSTM(64),
            layers.Dropout(0.3),
            
            # Dense layers for classification
            layers.Dense(128, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.4),
            
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.3),
            
            # Output layer
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        # Compile model
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        return model
    
    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        epochs: int = 100,
        batch_size: int = 32
    ):
        """
        Train the model
        
        Args:
            X_train: Training features
            y_train: Training labels
            X_val: Validation features
            y_val: Validation labels
            epochs: Number of training epochs
            batch_size: Batch size
        """
        # Callbacks
        callbacks = [
            keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=15,
                restore_best_weights=True
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7
            ),
            keras.callbacks.ModelCheckpoint(
                'saved_models/best_model.keras',
                monitor='val_accuracy',
                save_best_only=True,
                mode='max'
            )
        ]
        
        # Train
        logger.info("Starting training...")
        self.history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=1
        )
        
        logger.info("Training completed!")
    
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray):
        """Evaluate model on test set"""
        loss, accuracy = self.model.evaluate(X_test, y_test, verbose=0)
        logger.info(f"Test Loss: {loss:.4f}")
        logger.info(f"Test Accuracy: {accuracy:.4f}")
        return loss, accuracy

def load_savee_dataset(data_dir: str = 'data/SAVEE'):
    """
    Load SAVEE dataset
    
    Args:
        data_dir: Path to SAVEE dataset directory
    
    Returns:
        Tuple of (features, labels, emotion_map)
    """
    # SAVEE emotion mapping
    emotion_map = {
        'a': 'anger',
        'd': 'disgust',
        'f': 'fear',
        'h': 'happiness',
        'n': 'neutral',
        'sa': 'sadness',
        'su': 'surprise'
    }
    
    preprocessor = AudioPreprocessor()
    features = []
    labels = []
    
    logger.info(f"Loading dataset from {data_dir}")
    
    # Get all audio files
    audio_files = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.wav'):
                audio_files.append(os.path.join(root, file))
    
    logger.info(f"Found {len(audio_files)} audio files")
    
    # Process each file
    for file_path in tqdm(audio_files, desc="Processing audio files"):
        try:
            # Extract emotion from filename
            filename = os.path.basename(file_path)
            
            # SAVEE naming: [speaker]_[emotion][number].wav
            # e.g., DC_a01.wav, JE_h12.wav
            emotion_code = filename.split('_')[1][:2] if filename.split('_')[1][:2] in emotion_map else filename.split('_')[1][0]
            
            if emotion_code not in emotion_map:
                continue
            
            emotion = emotion_map[emotion_code]
            
            # Extract features
            mfcc, mel_spec = preprocessor.extract_features(file_path)
            
            # Combine features
            combined_features = np.concatenate([mfcc, mel_spec], axis=0)
            
            features.append(combined_features.T)  # Transpose to (time_steps, features)
            labels.append(emotion)
            
        except Exception as e:
            logger.warning(f"Error processing {file_path}: {str(e)}")
            continue
    
    logger.info(f"Successfully processed {len(features)} files")
    
    return np.array(features), np.array(labels), emotion_map

def main():
    """Main training pipeline"""
    
    # Create directories
    os.makedirs('saved_models', exist_ok=True)
    
    # Load dataset
    logger.info("Loading SAVEE dataset...")
    X, y, emotion_map = load_savee_dataset()
    
    # Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    logger.info(f"Dataset shape: {X.shape}")
    logger.info(f"Number of classes: {len(label_encoder.classes_)}")
    logger.info(f"Classes: {label_encoder.classes_}")
    
    # Split dataset
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y_encoded, test_size=0.3, random_state=42, stratify=y_encoded
    )
    
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
    )
    
    logger.info(f"Train set: {X_train.shape}")
    logger.info(f"Validation set: {X_val.shape}")
    logger.info(f"Test set: {X_test.shape}")
    
    # Build and train model
    model_builder = EmotionRecognitionModel(
        input_shape=X_train.shape[1:],
        num_classes=len(label_encoder.classes_)
    )
    
    model_builder.build_model()
    logger.info("Model architecture:")
    model_builder.model.summary()
    
    # Train
    model_builder.train(
        X_train, y_train,
        X_val, y_val,
        epochs=100,
        batch_size=32
    )
    
    # Evaluate
    logger.info("\nEvaluating on test set...")
    model_builder.evaluate(X_test, y_test)
    
    # Save model and label encoder
    logger.info("Saving model and label encoder...")
    model_builder.model.save('saved_models/emotion_model.keras')
    
    with open('saved_models/label_encoder.pkl', 'wb') as f:
        pickle.dump(label_encoder, f)
    
    # Save training history
    with open('saved_models/training_history.json', 'w') as f:
        history_dict = {
            'loss': [float(x) for x in model_builder.history.history['loss']],
            'accuracy': [float(x) for x in model_builder.history.history['accuracy']],
            'val_loss': [float(x) for x in model_builder.history.history['val_loss']],
            'val_accuracy': [float(x) for x in model_builder.history.history['val_accuracy']]
        }
        json.dump(history_dict, f, indent=2)
    
    logger.info("Training complete! Model saved to saved_models/")

if __name__ == "__main__":
    main()