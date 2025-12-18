# 🎙️ Speech Emotion Recognition for Customer Satisfaction

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)](https://www.tensorflow.org/)

An AI-powered system that analyzes customer emotions from speech to measure and improve customer satisfaction. Built with state-of-the-art deep learning models and a beautiful, intuitive interface.

![Speech Emotion Recognition Demo](docs/images/demo.png)

## 🌟 Features

- **Real-time Emotion Detection** - Analyze emotions from live audio or uploaded files
- **7 Emotion Classes** - Anger, Disgust, Fear, Happiness, Sadness, Surprise, Neutral
- **Customer Satisfaction Dashboard** - Visual analytics and insights
- **Beautiful UI** - Modern, responsive design with smooth animations
- **REST API** - Easy integration with existing systems
- **Production Ready** - Deployed and scalable architecture

## 🎯 Use Cases

- **Customer Service Analysis** - Measure satisfaction in support calls
- **Quality Assurance** - Monitor agent performance and customer sentiment
- **Product Feedback** - Understand emotional responses to products
- **User Experience Research** - Gather authentic emotional data

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- pip and npm

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/IshanDey007/speech-emotion-recognition.git
cd speech-emotion-recognition
```

2. **Set up the backend**
```bash
cd backend
pip install -r requirements.txt
python download_dataset.py  # Downloads SAVEE dataset
python train_model.py       # Trains the model
```

3. **Set up the frontend**
```bash
cd ../frontend
npm install
```

4. **Run the application**

Backend:
```bash
cd backend
uvicorn main:app --reload --port 8000
```

Frontend:
```bash
cd frontend
npm run dev
```

Visit `http://localhost:3000` to use the application!

## 📊 Model Architecture

Our model uses a hybrid CNN-LSTM architecture optimized for speech emotion recognition:

- **Input**: Audio files (WAV format)
- **Feature Extraction**: MFCC (Mel-Frequency Cepstral Coefficients) + Mel-Spectrogram
- **Model**: Convolutional layers → LSTM layers → Dense layers
- **Output**: 7 emotion probabilities

**Performance Metrics:**
- Accuracy: ~85% on SAVEE dataset
- F1-Score: 0.83 (weighted average)
- Inference Time: <100ms per audio file

## 🏗️ Project Structure

```
speech-emotion-recognition/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── model/
│   │   ├── train_model.py      # Model training script
│   │   ├── predict.py          # Prediction logic
│   │   └── preprocessing.py    # Audio preprocessing
│   ├── data/
│   │   └── SAVEE/              # Dataset directory
│   ├── saved_models/           # Trained model files
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── page.tsx            # Main page
│   │   ├── layout.tsx          # Root layout
│   │   └── api/                # API routes
│   ├── components/
│   │   ├── AudioRecorder.tsx   # Recording component
│   │   ├── EmotionChart.tsx    # Visualization
│   │   └── Dashboard.tsx       # Analytics dashboard
│   ├── public/
│   └── package.json
├── docs/
│   ├── API.md                  # API documentation
│   ├── MODEL.md                # Model architecture details
│   └── DEPLOYMENT.md           # Deployment guide
└── README.md
```

## 📖 Documentation

- [API Documentation](docs/API.md) - Complete API reference
- [Model Architecture](docs/MODEL.md) - Deep dive into the ML model
- [Deployment Guide](docs/DEPLOYMENT.md) - How to deploy to production
- [Dataset Information](docs/DATASET.md) - About the SAVEE dataset

## 🔧 API Usage

### Predict Emotion from Audio

```bash
curl -X POST "http://localhost:8000/api/predict" \
  -F "file=@audio.wav"
```

Response:
```json
{
  "emotion": "happiness",
  "confidence": 0.89,
  "probabilities": {
    "anger": 0.02,
    "disgust": 0.01,
    "fear": 0.03,
    "happiness": 0.89,
    "sadness": 0.01,
    "surprise": 0.03,
    "neutral": 0.01
  },
  "satisfaction_score": 8.5
}
```

## 🎨 UI Features

- **Drag & Drop Upload** - Easy audio file upload
- **Live Recording** - Record directly in browser
- **Real-time Visualization** - See emotion probabilities as charts
- **History Tracking** - View past analyses
- **Satisfaction Metrics** - Aggregate customer satisfaction scores
- **Dark/Light Mode** - Comfortable viewing experience

## 🧪 Testing

Run backend tests:
```bash
cd backend
pytest tests/
```

Run frontend tests:
```bash
cd frontend
npm test
```

## 📈 Performance Optimization

- **Model Quantization** - Reduced model size by 75%
- **Caching** - Redis integration for faster responses
- **Batch Processing** - Handle multiple files efficiently
- **CDN Integration** - Fast asset delivery

## 🌐 Deployment

### Deploy to Vercel (Frontend)

```bash
cd frontend
vercel deploy --prod
```

### Deploy Backend (Railway/Render)

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed instructions.

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **SAVEE Dataset** - Surrey Audio-Visual Expressed Emotion database
- **Research Paper** - "Speech Emotion Recognition for Power Customer Service"
- **365 Data Science** - Project inspiration

## 📧 Contact

Ishan Dey - irock9431@gmail.com

Project Link: [https://github.com/IshanDey007/speech-emotion-recognition](https://github.com/IshanDey007/speech-emotion-recognition)

---

Made with ❤️ for better customer experiences