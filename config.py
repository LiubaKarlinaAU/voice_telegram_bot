"""
Configuration settings for the Telegram PDF to MP3 bot.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
GROQ_TOKEN = os.getenv('GROQ_TOKEN')

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

# Validation
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required")

if not GROQ_TOKEN:
    raise ValueError("GROQ_TOKEN environment variable is required")
