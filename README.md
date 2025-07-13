# Mia Avatar AI Backend

A sophisticated AI-powered backend system for the beautiful, intelligent Mia Avatar - providing natural conversation, multilingual support, and comprehensive XETA product expertise.

## 🌟 Features

### 🤖 Advanced AI Capabilities
- **Natural Language Understanding**: Sophisticated conversation processing
- **XETA Product Expertise**: Comprehensive knowledge of XETA products and services
- **Intelligent Response Generation**: Context-aware and helpful responses
- **Intent Recognition**: Accurate understanding of user queries and needs

### 🌍 Multilingual Support
- **English & Spanish**: Full bilingual conversation capabilities
- **Cultural Adaptation**: Culturally appropriate responses and communication styles
- **Dynamic Language Switching**: Seamless language detection and switching
- **Localized Content**: Region-specific information and support

### 🎵 Voice Synthesis Integration
- **ElevenLabs Integration**: High-quality voice synthesis capabilities
- **Natural Speech**: Realistic voice generation with emotional expression
- **Multiple Voice Options**: Support for different voice types and styles
- **Audio Response**: Convert text responses to natural speech

### 🏢 XETA Integration
- **Product Knowledge**: Complete XETA Starter Kit information
- **Installation Guides**: Step-by-step setup instructions
- **Troubleshooting**: Comprehensive problem-solving assistance
- **Earning Information**: Detailed XETA token earning opportunities

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip package manager
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mia-avatar-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   python src/main.py
   ```

The API will be available at `http://localhost:5001`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
PORT=5001

# CORS Configuration
CORS_ORIGINS=*

# ElevenLabs Voice Synthesis (Optional)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# OpenAI Integration (Optional)
OPENAI_API_KEY=your_openai_api_key_here

# Database Configuration (if needed)
DATABASE_URL=sqlite:///mia_avatar.db
```

### Required Environment Variables
- `PORT`: Port number for the Flask application (default: 5001)
- `CORS_ORIGINS`: Allowed origins for CORS (use * for development)

### Optional Environment Variables
- `ELEVENLABS_API_KEY`: For voice synthesis functionality
- `OPENAI_API_KEY`: For enhanced AI responses
- `FLASK_DEBUG`: Set to True for development mode

## 📚 API Documentation

### Base URL
```
http://localhost:5001
```

### Endpoints

#### Health Check
```http
GET /
```
Returns API status and version information.

#### Conversation Chat
```http
POST /api/conversation/chat
Content-Type: application/json

{
  "message": "Hello, I need help with XETA installation",
  "language": "en"
}
```

#### Voice Synthesis
```http
POST /api/voice/synthesize
Content-Type: application/json

{
  "text": "Hello, how can I help you today?",
  "voice": "female_voice"
}
```

#### Knowledge Base Query
```http
POST /api/knowledge/query
Content-Type: application/json

{
  "query": "XETA installation steps",
  "language": "en"
}
```

#### Avatar Status
```http
GET /api/avatar/status
```

#### Integrated Chat (Recommended)
```http
POST /api/integrated/chat
Content-Type: application/json

{
  "message": "How do I install XETA?",
  "language": "en",
  "include_voice": true
}
```

## 🏗️ Architecture

### Project Structure
```
src/
├── main.py                 # Application entry point
├── models/                 # AI models and logic
│   ├── conversation_ai.py  # Main conversation handling
│   ├── voice_synthesis.py  # Voice generation
│   ├── multilingual_support.py # Language processing
│   └── tech_support_knowledge.py # Knowledge base
└── routes/                 # API route handlers
    ├── conversation.py     # Chat endpoints
    ├── voice.py           # Voice synthesis endpoints
    ├── knowledge.py       # Knowledge base endpoints
    ├── avatar.py          # Avatar status endpoints
    └── integrated_chat.py # Combined functionality
```

### Key Components

#### Conversation AI (`models/conversation_ai.py`)
- Natural language processing
- Intent recognition and response generation
- Context management and conversation flow

#### Voice Synthesis (`models/voice_synthesis.py`)
- ElevenLabs API integration
- Voice generation and audio processing
- Multiple voice type support

#### Multilingual Support (`models/multilingual_support.py`)
- Language detection and switching
- Cultural adaptation and localization
- Bilingual conversation management

#### Knowledge Base (`models/tech_support_knowledge.py`)
- XETA product information
- Troubleshooting guides and solutions
- Installation and setup instructions

## 🌐 Deployment

### Local Development
```bash
python src/main.py
```

### Production Deployment

#### Using Gunicorn
```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:5001 --workers 4 src.main:app
```

#### Using Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
EXPOSE 5001
CMD ["python", "src/main.py"]
```

#### Environment-Specific Configuration
- **Development**: Set `FLASK_DEBUG=True`
- **Production**: Set `FLASK_ENV=production`
- **CORS**: Configure appropriate origins for security

## 🔒 Security

### Best Practices
- Store API keys in environment variables
- Use HTTPS in production
- Configure CORS appropriately
- Validate all input data
- Implement rate limiting for production use

### API Key Management
- Never commit API keys to version control
- Use environment variables for all secrets
- Rotate API keys regularly
- Monitor API usage and costs

## 🧪 Testing

### Run Tests
```bash
# Install test dependencies
pip install pytest pytest-flask

# Run tests
pytest tests/
```

### API Testing
Use tools like Postman, curl, or HTTPie to test endpoints:

```bash
# Test health endpoint
curl http://localhost:5001/

# Test conversation
curl -X POST http://localhost:5001/api/conversation/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "language": "en"}'
```

## 📊 Monitoring

### Health Checks
- GET `/` - Basic health check
- GET `/api/avatar/status` - Detailed system status

### Logging
- Application logs are written to console
- Configure log levels via environment variables
- Monitor API response times and error rates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add tests for new functionality
- Update documentation for API changes
- Use meaningful commit messages

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Documentation
- API Documentation: See endpoints section above
- Knowledge Base: Comprehensive XETA product information included
- Troubleshooting: Common issues and solutions in docs/

### Contact
- Issues: Use GitHub Issues for bug reports and feature requests
- Discussions: Use GitHub Discussions for questions and community support

## 🎯 Roadmap

### Upcoming Features
- Enhanced AI conversation capabilities
- Additional language support
- Advanced voice synthesis options
- Improved XETA product integration
- Performance optimizations

### Version History
- v1.0.0: Initial release with core functionality
- Multilingual support and XETA integration
- Voice synthesis and conversation AI

---

**Mia Avatar AI Backend** - Powering intelligent, beautiful, and multilingual customer service experiences.

