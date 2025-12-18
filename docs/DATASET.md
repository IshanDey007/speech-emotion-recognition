# SAVEE Dataset Documentation

Complete information about the Surrey Audio-Visual Expressed Emotion (SAVEE) dataset used for training.

## Overview

**SAVEE** (Surrey Audio-Visual Expressed Emotion) is a high-quality audio-visual database of emotional expressions designed for emotion recognition research.

- **Institution**: University of Surrey, UK
- **Year**: 2008
- **Type**: Audio-Visual
- **Language**: English
- **Recording**: Studio quality

## Dataset Statistics

| Attribute | Value |
|-----------|-------|
| Total Utterances | 480 |
| Speakers | 4 (all male) |
| Emotions | 7 classes |
| Duration per clip | ~2-3 seconds |
| Sample Rate | 44.1 kHz (original) |
| Format | WAV |
| Total Size | ~150 MB |

## Emotion Classes

### Distribution

| Emotion | Code | Count | Percentage | Description |
|---------|------|-------|------------|-------------|
| **Anger** | `a` | 60 | 12.5% | Frustrated, angry expressions |
| **Disgust** | `d` | 60 | 12.5% | Expressions of disgust |
| **Fear** | `f` | 60 | 12.5% | Fearful, anxious expressions |
| **Happiness** | `h` | 60 | 12.5% | Happy, joyful expressions |
| **Neutral** | `n` | 120 | 25.0% | Neutral, emotionless speech |
| **Sadness** | `sa` | 60 | 12.5% | Sad, unhappy expressions |
| **Surprise** | `su` | 60 | 12.5% | Surprised reactions |

**Note**: Neutral has double the samples (120) compared to other emotions (60 each).

## Speakers

### Speaker Information

| Speaker ID | Gender | Age Range | Accent |
|------------|--------|-----------|--------|
| DC | Male | 30-35 | British English |
| JE | Male | 30-35 | British English |
| JK | Male | 30-35 | British English |
| KL | Male | 30-35 | British English |

**Limitation**: All speakers are male, which may affect generalization to female voices.

## File Naming Convention

Files follow the pattern: `[Speaker]_[Emotion][Number].wav`

### Examples

- `DC_a01.wav` - Speaker DC, Anger, utterance 1
- `JE_h12.wav` - Speaker JE, Happiness, utterance 12
- `KL_n05.wav` - Speaker KL, Neutral, utterance 5
- `JK_sa08.wav` - Speaker JK, Sadness, utterance 8

### Emotion Codes

```
a   → anger
d   → disgust
f   → fear
h   → happiness
n   → neutral
sa  → sadness
su  → surprise
```

## Utterances

### Sample Sentences

The dataset includes various sentence types:

**Emotionally Neutral Sentences:**
- "The boy went to the store"
- "She had your dark suit in greasy wash water all year"
- "Don't ask me to carry an oily rag like that"

**Emotionally Charged Sentences:**
- "I'm so angry I could scream!" (anger)
- "That's absolutely disgusting!" (disgust)
- "I'm terrified of what might happen" (fear)
- "This is the best day ever!" (happiness)
- "I feel so sad and alone" (sadness)
- "Wow, I can't believe it!" (surprise)

## Recording Specifications

### Audio Specifications

- **Sample Rate**: 44,100 Hz (original)
- **Bit Depth**: 16-bit
- **Channels**: Mono
- **Format**: Uncompressed WAV
- **Recording Environment**: Anechoic chamber (minimal echo)
- **Microphone**: High-quality condenser microphone

### Video Specifications (Not Used)

- **Resolution**: 720x576 pixels
- **Frame Rate**: 60 fps
- **Format**: AVI
- **Note**: Our project uses audio only

## Data Quality

### Strengths

✅ **High Audio Quality**
- Professional studio recording
- Minimal background noise
- Clear articulation

✅ **Controlled Environment**
- Consistent recording conditions
- Standardized setup
- Professional actors

✅ **Balanced Distribution**
- Equal samples per emotion (except neutral)
- Multiple speakers
- Varied utterances

### Limitations

⚠️ **Limited Diversity**
- Only 4 speakers
- All male speakers
- Single language (English)
- British accent only

⚠️ **Small Dataset**
- 480 total samples
- May lead to overfitting
- Limited generalization

⚠️ **Acted Emotions**
- Not spontaneous emotions
- May differ from real-world scenarios
- Professional actors (not typical speakers)

## Download Instructions

### Official Source

1. Visit: http://kahlan.eps.surrey.ac.uk/savee/
2. Register for access
3. Download the dataset
4. Extract files

### Alternative Sources

- **Kaggle**: Search for "SAVEE dataset"
- **GitHub**: Various repositories host the dataset
- **Academic Institutions**: Contact University of Surrey

### Using Our Download Script

```bash
cd backend
python download_dataset.py
```

This will:
- Show download instructions
- Check if dataset exists
- Provide file structure guidance

### Creating Sample Dataset (For Testing)

```bash
python download_dataset.py --sample
```

This creates synthetic audio files for testing without downloading the full dataset.

## Data Preprocessing

### Our Pipeline

1. **Loading**
   ```python
   audio, sr = librosa.load(file_path, sr=22050, duration=3.0)
   ```

2. **Normalization**
   ```python
   audio = audio / (np.max(np.abs(audio)) + 1e-6)
   ```

3. **Padding/Trimming**
   ```python
   if len(audio) < max_length:
       audio = np.pad(audio, (0, max_length - len(audio)))
   else:
       audio = audio[:max_length]
   ```

4. **Feature Extraction**
   - MFCC (40 coefficients)
   - Mel-Spectrogram (128 bands)

## Data Splits

### Our Split Strategy

```python
# 70% Training, 15% Validation, 15% Test
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
)
```

### Split Distribution

| Split | Samples | Percentage |
|-------|---------|------------|
| Training | 336 | 70% |
| Validation | 72 | 15% |
| Testing | 72 | 15% |

**Stratified Split**: Maintains emotion distribution across all splits.

## Data Augmentation

### Techniques Used (Optional)

1. **White Noise Addition**
   ```python
   noise = np.random.randn(len(audio))
   audio_noise = audio + 0.005 * noise
   ```

2. **Pitch Shifting**
   ```python
   audio_shifted = librosa.effects.pitch_shift(audio, sr=sr, n_steps=2)
   ```

3. **Time Stretching**
   ```python
   audio_stretched = librosa.effects.time_stretch(audio, rate=1.1)
   ```

## Citation

If you use the SAVEE dataset, please cite:

```bibtex
@inproceedings{haq2008audio,
  title={Audio-visual feature selection and reduction for emotion classification},
  author={Haq, Sanaul and Jackson, Philip JB},
  booktitle={Proc. Int'l Conf. on Auditory-Visual Speech Processing (AVSP'08)},
  pages={185--190},
  year={2008},
  organization={Tangalooma, Australia}
}
```

## Related Datasets

For comparison or additional training:

| Dataset | Emotions | Samples | Language | Type |
|---------|----------|---------|----------|------|
| **RAVDESS** | 8 | 7,356 | English | Audio-Visual |
| **IEMOCAP** | 10 | 10,039 | English | Audio-Visual |
| **EMO-DB** | 7 | 535 | German | Audio |
| **CREMA-D** | 6 | 7,442 | English | Audio-Visual |
| **TESS** | 7 | 2,800 | English | Audio |

## License

The SAVEE dataset is available for academic research purposes. Check the official website for licensing terms.

## Support

For dataset-related questions:
- Official Website: http://kahlan.eps.surrey.ac.uk/savee/
- Project Issues: https://github.com/IshanDey007/speech-emotion-recognition/issues
- Email: irock9431@gmail.com

---

**Last Updated**: December 2025