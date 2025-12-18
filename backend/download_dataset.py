"""
SAVEE Dataset Download Script
Downloads and prepares the SAVEE dataset for training
"""

import os
import urllib.request
import zipfile
import logging
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DownloadProgressBar(tqdm):
    """Progress bar for downloads"""
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def download_url(url: str, output_path: str):
    """Download file with progress bar"""
    with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)

def download_savee_dataset(data_dir: str = 'data'):
    """
    Download SAVEE dataset
    
    Note: SAVEE dataset is available from:
    http://kahlan.eps.surrey.ac.uk/savee/
    
    For this project, we'll provide instructions for manual download
    as the dataset requires registration.
    """
    
    os.makedirs(data_dir, exist_ok=True)
    savee_dir = os.path.join(data_dir, 'SAVEE')
    
    logger.info("=" * 70)
    logger.info("SAVEE Dataset Download Instructions")
    logger.info("=" * 70)
    logger.info("")
    logger.info("The SAVEE (Surrey Audio-Visual Expressed Emotion) dataset")
    logger.info("requires manual download from the official source.")
    logger.info("")
    logger.info("Steps to download:")
    logger.info("1. Visit: http://kahlan.eps.surrey.ac.uk/savee/")
    logger.info("2. Register and download the dataset")
    logger.info("3. Extract the downloaded files")
    logger.info(f"4. Place all .wav files in: {os.path.abspath(savee_dir)}")
    logger.info("")
    logger.info("Dataset structure:")
    logger.info("  data/SAVEE/")
    logger.info("    ├── DC_a01.wav")
    logger.info("    ├── DC_a02.wav")
    logger.info("    ├── ...")
    logger.info("    └── [speaker]_[emotion][number].wav")
    logger.info("")
    logger.info("Emotion codes:")
    logger.info("  a  = anger")
    logger.info("  d  = disgust")
    logger.info("  f  = fear")
    logger.info("  h  = happiness")
    logger.info("  n  = neutral")
    logger.info("  sa = sadness")
    logger.info("  su = surprise")
    logger.info("")
    logger.info("Total files: 480 utterances from 4 male speakers")
    logger.info("=" * 70)
    
    # Create SAVEE directory
    os.makedirs(savee_dir, exist_ok=True)
    
    # Check if dataset already exists
    wav_files = [f for f in os.listdir(savee_dir) if f.endswith('.wav')] if os.path.exists(savee_dir) else []
    
    if len(wav_files) > 0:
        logger.info(f"\n✓ Found {len(wav_files)} audio files in {savee_dir}")
        logger.info("Dataset appears to be already downloaded!")
        return True
    else:
        logger.info(f"\n✗ No audio files found in {savee_dir}")
        logger.info("Please download the dataset following the instructions above.")
        return False

def create_sample_dataset(data_dir: str = 'data'):
    """
    Create a small sample dataset for testing
    This generates synthetic audio files for development/testing
    """
    import numpy as np
    import soundfile as sf
    
    logger.info("Creating sample dataset for testing...")
    
    savee_dir = os.path.join(data_dir, 'SAVEE')
    os.makedirs(savee_dir, exist_ok=True)
    
    # Emotion codes
    emotions = ['a', 'd', 'f', 'h', 'n', 'sa', 'su']
    speakers = ['DC', 'JE', 'JK', 'KL']
    
    sample_rate = 22050
    duration = 3  # seconds
    
    # Generate sample files
    count = 0
    for speaker in speakers:
        for emotion in emotions:
            for i in range(1, 6):  # 5 samples per emotion per speaker
                # Generate random audio (white noise)
                audio = np.random.randn(sample_rate * duration) * 0.1
                
                # Add some frequency components to make it more realistic
                t = np.linspace(0, duration, sample_rate * duration)
                audio += 0.05 * np.sin(2 * np.pi * 440 * t)  # A4 note
                
                # Normalize
                audio = audio / np.max(np.abs(audio))
                
                # Save file
                filename = f"{speaker}_{emotion}{i:02d}.wav"
                filepath = os.path.join(savee_dir, filename)
                sf.write(filepath, audio, sample_rate)
                count += 1
    
    logger.info(f"✓ Created {count} sample audio files in {savee_dir}")
    logger.info("Note: These are synthetic files for testing only!")
    logger.info("For real training, please download the actual SAVEE dataset.")
    
    return True

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Download SAVEE dataset')
    parser.add_argument('--sample', action='store_true', 
                       help='Create sample dataset for testing')
    parser.add_argument('--data-dir', type=str, default='data',
                       help='Directory to store dataset')
    
    args = parser.parse_args()
    
    if args.sample:
        create_sample_dataset(args.data_dir)
    else:
        download_savee_dataset(args.data_dir)

if __name__ == "__main__":
    main()