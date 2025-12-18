# API Documentation

Complete API reference for the Speech Emotion Recognition system.

## Base URL

```
http://localhost:8000
```

For production, replace with your deployed backend URL.

## Authentication

Currently, the API does not require authentication. For production deployment, consider implementing API keys or OAuth.

## Endpoints

### Health Check

#### GET `/`

Check if the API is running and model is loaded.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

---

### Predict Emotion

#### POST `/api/predict`

Analyze emotion from a single audio file.

**Request:**
- Content-Type: `multipart/form-data`
- Body: Form data with `file` field containing audio file

**Supported Formats:**
- WAV (.wav)
- MP3 (.mp3)
- FLAC (.flac)
- OGG (.ogg)

**Example (cURL):**
```bash
curl -X POST "http://localhost:8000/api/predict" \
  -F "file=@customer_call.wav"
```

**Example (Python):**
```python
import requests

url = "http://localhost:8000/api/predict"
files = {"file": open("customer_call.wav", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

**Example (JavaScript):**
```javascript
const formData = new FormData();
formData.append('file', audioFile);

const response = await fetch('http://localhost:8000/api/predict', {
  method: 'POST',
  body: formData
});

const data = await response.json();
console.log(data);
```

**Response:**
```json
{
  "emotion": "happiness",
  "confidence": 0.8945,
  "probabilities": {
    "anger": 0.0234,
    "disgust": 0.0123,
    "fear": 0.0345,
    "happiness": 0.8945,
    "sadness": 0.0156,
    "surprise": 0.0134,
    "neutral": 0.0063
  },
  "satisfaction_score": 8.5,
  "timestamp": "2025-12-18T04:30:00.000Z"
}
```

**Response Fields:**
- `emotion` (string): Detected primary emotion
- `confidence` (float): Confidence score for primary emotion (0-1)
- `probabilities` (object): Probability distribution across all emotions
- `satisfaction_score` (float): Customer satisfaction score (0-10)
- `timestamp` (string): ISO 8601 timestamp of analysis

**Error Responses:**

400 Bad Request:
```json
{
  "detail": "Unsupported file type. Allowed: .wav, .mp3, .flac, .ogg"
}
```

503 Service Unavailable:
```json
{
  "detail": "Model not loaded. Please train the model first."
}
```

---

### Batch Prediction

#### POST `/api/predict/batch`

Analyze emotions from multiple audio files in one request.

**Request:**
- Content-Type: `multipart/form-data`
- Body: Form data with multiple `files` fields (max 10 files)

**Example (cURL):**
```bash
curl -X POST "http://localhost:8000/api/predict/batch" \
  -F "files=@call1.wav" \
  -F "files=@call2.wav" \
  -F "files=@call3.wav"
```

**Example (Python):**
```python
import requests

url = "http://localhost:8000/api/predict/batch"
files = [
    ("files", open("call1.wav", "rb")),
    ("files", open("call2.wav", "rb")),
    ("files", open("call3.wav", "rb"))
]
response = requests.post(url, files=files)
print(response.json())
```

**Response:**
```json
{
  "results": [
    {
      "emotion": "happiness",
      "confidence": 0.8945,
      "probabilities": {...},
      "satisfaction_score": 8.5,
      "timestamp": "2025-12-18T04:30:00.000Z"
    },
    {
      "emotion": "neutral",
      "confidence": 0.7234,
      "probabilities": {...},
      "satisfaction_score": 6.2,
      "timestamp": "2025-12-18T04:30:01.000Z"
    }
  ],
  "average_satisfaction": 7.35
}
```

**Limitations:**
- Maximum 10 files per request
- Each file must be under 10MB

---

### Get Supported Emotions

#### GET `/api/emotions`

Get list of emotions the model can detect.

**Response:**
```json
{
  "emotions": [
    "anger",
    "disgust",
    "fear",
    "happiness",
    "sadness",
    "surprise",
    "neutral"
  ],
  "count": 7
}
```

---

### Get API Statistics

#### GET `/api/stats`

Get API configuration and statistics.

**Response:**
```json
{
  "model_loaded": true,
  "supported_emotions": 7,
  "max_batch_size": 10,
  "supported_formats": [".wav", ".mp3", ".flac", ".ogg"]
}
```

---

## Emotion Classes

The model detects 7 distinct emotions:

| Emotion | Description | Satisfaction Impact |
|---------|-------------|-------------------|
| **Happiness** | Positive, joyful emotion | High (9.0) |
| **Surprise** | Unexpected reaction | Medium-High (7.0) |
| **Neutral** | No strong emotion | Medium (6.0) |
| **Sadness** | Negative, unhappy emotion | Low (3.0) |
| **Fear** | Anxious, worried emotion | Low (2.5) |
| **Disgust** | Strong negative reaction | Low (2.0) |
| **Anger** | Frustrated, angry emotion | Very Low (1.0) |

---

## Satisfaction Score Calculation

The satisfaction score (0-10) is calculated based on:

1. **Base Score**: Each emotion has a base satisfaction score
2. **Confidence Adjustment**: Score is weighted by prediction confidence
3. **Formula**: `base_score * confidence + 5.0 * (1 - confidence)`

This ensures that:
- High confidence in positive emotions = high satisfaction
- High confidence in negative emotions = low satisfaction
- Low confidence predictions trend toward neutral (5.0)

---

## Rate Limiting

Currently no rate limiting is implemented. For production:

- Recommended: 100 requests per minute per IP
- Batch endpoint: 10 requests per minute per IP
- Consider implementing Redis-based rate limiting

---

## Error Handling

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Common HTTP Status Codes:**
- `200`: Success
- `400`: Bad Request (invalid input)
- `422`: Validation Error
- `500`: Internal Server Error
- `503`: Service Unavailable (model not loaded)

---

## Best Practices

1. **File Size**: Keep audio files under 10MB for faster processing
2. **Duration**: 3-5 second clips work best
3. **Quality**: Higher quality audio = better accuracy
4. **Format**: WAV format recommended for best results
5. **Batch Processing**: Use batch endpoint for multiple files to reduce overhead

---

## Integration Examples

### Customer Service Dashboard

```python
import requests
import os

def analyze_customer_call(audio_path):
    """Analyze customer service call recording"""
    url = "http://localhost:8000/api/predict"
    
    with open(audio_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Emotion: {result['emotion']}")
        print(f"Satisfaction: {result['satisfaction_score']}/10")
        return result
    else:
        print(f"Error: {response.json()['detail']}")
        return None

# Usage
result = analyze_customer_call("customer_call.wav")
```

### Real-time Monitoring

```javascript
async function monitorCustomerSatisfaction(audioFiles) {
  const formData = new FormData();
  
  audioFiles.forEach(file => {
    formData.append('files', file);
  });
  
  const response = await fetch('http://localhost:8000/api/predict/batch', {
    method: 'POST',
    body: formData
  });
  
  const data = await response.json();
  
  console.log(`Average Satisfaction: ${data.average_satisfaction}/10`);
  
  // Alert if satisfaction is low
  if (data.average_satisfaction < 5) {
    alert('Low customer satisfaction detected!');
  }
  
  return data;
}
```

---

## Support

For issues or questions:
- GitHub Issues: https://github.com/IshanDey007/speech-emotion-recognition/issues
- Email: irock9431@gmail.com