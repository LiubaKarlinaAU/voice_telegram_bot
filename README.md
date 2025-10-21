# 🤖 Telegram PDF to MP3 Bot

A powerful Telegram bot that converts PDF documents to MP3 audio files using multiple TTS (Text-to-Speech) models.

## ✨ Features

- **Dual TTS Models**: Choose between Google TTS and Groq AI
- **Interactive UI**: Beautiful buttons and menus
- **Multi-language Support**: Handles Russian, English, and more
- **Smart Processing**: AI-enhanced text processing with Groq
- **Free & Paid Options**: Google TTS (free) and Groq AI (enhanced)

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Telegram Bot Token
- Groq API Token (optional, for enhanced features)

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd telegram_bot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Create .env file
BOT_TOKEN=your_telegram_bot_token
GROQ_TOKEN=your_groq_api_token
```

4. **Run the bot**
```bash
python bot.py
```

## 🎯 Usage

### Commands
- `/start` - Interactive welcome with model selection
- `/help` - Comprehensive help guide
- `/pdf2mp3` - Convert PDF to MP3
- `/extract` - Extract text only
- `/tts_model` - Choose TTS model
- `/current_model` - Show current model

### TTS Models

#### 🇺🇸 Google TTS (Free)
- ✅ Free and fast
- ✅ Supports multiple languages
- ✅ Output in original language
- ✅ No API costs

#### 🤖 Groq AI (Enhanced)
- ✅ AI-enhanced text processing
- ✅ Can parse Russian → English
- ✅ Better speech quality
- ⚠️ Requires API credits

## 🏗️ Project Structure

```
telegram_bot/
├── bot.py              # Main bot file
├── config.py           # Configuration settings
├── handlers.py         # Bot command handlers
├── utils.py           # Text processing utilities
├── requirements.txt    # Python dependencies
├── Procfile           # Railway deployment
├── railway.json       # Railway configuration
├── runtime.txt        # Python version
└── DEPLOYMENT.md      # Deployment guide
```

## 🚀 Deployment

### Railway Cloud (Recommended)

1. **Connect to Railway**
   - Sign up at [railway.app](https://railway.app)
   - Connect your GitHub repository

2. **Set Environment Variables**
   - `BOT_TOKEN`: Your Telegram bot token
   - `GROQ_TOKEN`: Your Groq API token

3. **Deploy**
   - Railway auto-detects Python projects
   - Deploys automatically on git push

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### Other Platforms
- **Heroku**: Add `Procfile` and deploy
- **DigitalOcean**: Use App Platform
- **AWS**: Use Elastic Beanstalk
- **Google Cloud**: Use App Engine

## 🔧 Configuration

### Environment Variables
```bash
BOT_TOKEN=your_telegram_bot_token_here
GROQ_TOKEN=your_groq_api_token_here
```

### Model Settings
- **Default Model**: Google TTS (free)
- **Chunk Size**: 5000 chars (gTTS), 2000 chars (Groq)
- **Max Tokens**: 2000 (Groq)
- **Temperature**: 0.7 (Groq)

## 📊 Features

### Interactive UI
- Beautiful inline keyboards
- Model selection buttons
- Help navigation
- Real-time feedback

### Smart Processing
- PDF text extraction
- Chunk processing for large files
- Error handling and recovery
- Quota management

### Multi-language Support
- **Google TTS**: Supports 100+ languages
- **Groq AI**: Russian → English translation
- **Output**: Original language (gTTS) or English (Groq)

## 🛠️ Development

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run bot
python bot.py

# Test compilation
python -m py_compile bot.py config.py utils.py handlers.py
```

### Code Structure
- **Modular Design**: Separated concerns
- **Error Handling**: Comprehensive error management
- **Logging**: Detailed logging for debugging
- **Type Hints**: Python type annotations

## 📈 Monitoring

### Railway Dashboard
- View logs and metrics
- Monitor resource usage
- Check deployment status
- Set up alerts

### Bot Health
- Automatic restart on failure
- Error logging and reporting
- Performance monitoring
- User feedback tracking

## 🔒 Security

- Environment variables for sensitive data
- No hardcoded tokens
- Secure API communication
- Input validation and sanitization

## 📞 Support

- **Documentation**: See DEPLOYMENT.md
- **Issues**: GitHub Issues
- **Telegram**: Contact bot owner
- **Railway**: [docs.railway.app](https://docs.railway.app)

## 📄 License

This project is open source. Feel free to use and modify.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Made with ❤️ for the Telegram community**