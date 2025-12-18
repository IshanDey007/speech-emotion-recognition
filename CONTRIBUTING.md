# Contributing to Speech Emotion Recognition

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/IshanDey007/speech-emotion-recognition/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, Python version, etc.)

### Suggesting Features

1. Check existing [Issues](https://github.com/IshanDey007/speech-emotion-recognition/issues) for similar suggestions
2. Create a new issue with:
   - Clear feature description
   - Use case and benefits
   - Possible implementation approach

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/IshanDey007/speech-emotion-recognition.git
   cd speech-emotion-recognition
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow existing code style
   - Add tests if applicable
   - Update documentation

4. **Test your changes**
   ```bash
   # Backend tests
   cd backend
   pytest tests/
   
   # Frontend tests
   cd frontend
   npm test
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

   **Commit Message Format:**
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `style:` Code style changes
   - `refactor:` Code refactoring
   - `test:` Test additions/changes
   - `chore:` Build/config changes

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template
   - Link related issues

## Development Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Code Style

### Python (Backend)

- Follow [PEP 8](https://pep8.org/)
- Use type hints
- Add docstrings to functions
- Maximum line length: 100 characters

```python
def process_audio(file_path: str) -> Dict[str, float]:
    """
    Process audio file and extract features.
    
    Args:
        file_path: Path to audio file
    
    Returns:
        Dictionary of extracted features
    """
    pass
```

### TypeScript/React (Frontend)

- Use TypeScript for type safety
- Follow React best practices
- Use functional components with hooks
- Add JSDoc comments for complex functions

```typescript
/**
 * Analyze emotion from audio file
 * @param file - Audio file to analyze
 * @returns Promise with emotion analysis results
 */
async function analyzeEmotion(file: File): Promise<EmotionResult> {
  // Implementation
}
```

## Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Documentation

- Update README.md if adding features
- Add API documentation for new endpoints
- Update model documentation for architecture changes
- Include code comments for complex logic

## Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, PR will be merged
4. Your contribution will be credited

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## Questions?

- Open an issue for questions
- Email: irock9431@gmail.com
- Check existing documentation

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing! 🎉