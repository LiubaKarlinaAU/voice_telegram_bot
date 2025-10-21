"""
Configuration settings for the Telegram PDF to MP3 bot.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
GROQ_TOKEN = os.getenv('GROQ_TOKEN') or None  # Ensure it's None if not set

# TTS Model configuration
DEFAULT_TTS_MODEL = 'gtts'
AVAILABLE_MODELS = {
    'gtts': {
        'name': 'Google TTS',
        'description': 'Free and fast',
        'emoji': '🇺🇸',
        'features': [
            'Supports multiple languages (Russian, English, etc.)',
            'Output in original language',
            'No API costs'
        ]
    },
    'groq': {
        'name': 'Groq AI',
        'description': 'AI-enhanced text processing',
        'emoji': '🤖',
        'features': [
            'Can parse Russian text → English output',
            'Better speech quality',
            'Requires API credits'
        ]
    }
}

# Text processing limits
GTTTS_MAX_CHUNK_LENGTH = 5000
GROQ_MAX_CHUNK_LENGTH = 2000
GROQ_MAX_TOKENS = 2000
GROQ_TEMPERATURE = 0.7

# Validation - Only validate BOT_TOKEN if running locally
if not os.getenv('RAILWAY_ENVIRONMENT'):
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN environment variable is required")
    
    # GROQ_TOKEN is optional - bot can work with just gTTS
    if not GROQ_TOKEN:
        print("Warning: GROQ_TOKEN not set. Groq features will be disabled.")
