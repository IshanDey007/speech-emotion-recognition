# Quick Start Guide

Get the Speech Emotion Recognition system running in 5 minutes!

## Prerequisites

- Python 3.8+ installed
- Node.js 18+ installed
- Git installed

## Step 1: Clone Repository

```bash
git clone https://github.com/IshanDey007/speech-emotion-recognition.git
cd speech-emotion-recognition
```

## Step 2: Setup Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download/create sample dataset
python download_dataset.py --sample

# Train the model (this will take a few minutes)
cd model
python train_model.py
cd ..

# Start the backend server
uvicorn main:app --reload --port 8000
```

Backend will be running at `http://localhost:8000`

## Step 3: Setup Frontend (New Terminal)

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Start development server
npm run dev
```

Frontend will be running at `http://localhost:3000`

## Step 4: Test the Application

1. Open browser to `http://localhost:3000`
2. Upload an audio file (WAV, MP3, FLAC, or OGG)
3. Click "Analyze Emotion"
4. View results!

## Quick Test with Sample Audio

If you don't have audio files, you can:

1. Record a short voice message on your phone
2. Transfer it to your computer
3. Upload it to the application

Or use the sample files generated during training in `backend/data/SAVEE/`

## API Test

Test the API directly:

```bash
# Health check
curl http://localhost:8000/health

# Predict emotion (replace with your audio file)
curl -X POST "http://localhost:8000/api/predict" \
  -F "file=@path/to/your/audio.wav"
```

## Troubleshooting

### Backend Issues

**"Model not found"**
```bash
cd backend/model
python train_model.py
```

**"Module not found"**
```bash
pip install -r requirements.txt
```

**Port 8000 already in use**
```bash
uvicorn main:app --reload --port 8001
# Update NEXT_PUBLIC_API_URL in frontend/.env.local
```

### Frontend Issues

**"Cannot connect to API"**
- Ensure backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`

**"Module not found"**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Port 3000 already in use**
```bash
npm run dev -- -p 3001
```

## Next Steps

- Read the [full README](README.md) for detailed information
- Check [API Documentation](docs/API.md) for integration
- See [Model Documentation](docs/MODEL.md) for architecture details
- Review [Deployment Guide](docs/DEPLOYMENT.md) for production setup

## Need Help?

- GitHub Issues: https://github.com/IshanDey007/speech-emotion-recognition/issues
- Email: irock9431@gmail.com

Happy analyzing! 🎙️✨