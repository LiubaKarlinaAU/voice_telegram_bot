"""
Utility functions for text processing and TTS conversion.
"""
import os
import logging
import tempfile
import PyPDF2
from gtts import gTTS
from groq import Groq
from config import GROQ_TOKEN, GTTTS_MAX_CHUNK_LENGTH, GROQ_MAX_CHUNK_LENGTH, GROQ_MAX_TOKENS, GROQ_TEMPERATURE

logger = logging.getLogger(__name__)

# Initialize Groq client
groq_client = Groq(api_key=GROQ_TOKEN)

def extract_text_from_pdf(pdf_file_path):
    """Extract text from PDF file."""
    try:
        with open(pdf_file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        return None

def text_to_speech_gtts(text, output_path):
    """Convert text to speech using gTTS (Google Text-to-Speech)."""
    try:
        # Split text into chunks if it's too long (gTTS has limits)
        chunks = [text[i:i+GTTTS_MAX_CHUNK_LENGTH] for i in range(0, len(text), GTTTS_MAX_CHUNK_LENGTH)]
        
        audio_files = []
        for i, chunk in enumerate(chunks):
            if chunk.strip():  # Skip empty chunks
                # Create gTTS object
                tts = gTTS(text=chunk, lang='en', slow=False)
                
                chunk_path = f"{output_path}_part_{i}.mp3"
                tts.save(chunk_path)
                audio_files.append(chunk_path)
        
        return audio_files
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            logger.error(f"gTTS API quota exceeded: {e}")
            return "QUOTA_EXCEEDED"
        elif "insufficient_quota" in error_msg.lower():
            logger.error(f"gTTS API insufficient quota: {e}")
            return "QUOTA_EXCEEDED"
        else:
            logger.error(f"Error converting text to speech with gTTS: {e}")
            return None

def text_to_speech_groq(text, output_path):
    """Convert text to speech using Groq with llama-3.1-8b-instant model."""
    try:
        # Split text into chunks if it's too long
        chunks = [text[i:i+GROQ_MAX_CHUNK_LENGTH] for i in range(0, len(text), GROQ_MAX_CHUNK_LENGTH)]
        
        audio_files = []
        for i, chunk in enumerate(chunks):
            if chunk.strip():  # Skip empty chunks
                # Use Groq to generate speech-like text (since Groq doesn't have direct TTS)
                # We'll use it to enhance the text for better TTS conversion
                prompt = f"Convert this text into natural speech format, maintaining all important information but making it more conversational and suitable for text-to-speech: {chunk}"
                
                response = groq_client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "You are a text-to-speech assistant. Convert the given text into natural, conversational speech format that sounds good when read aloud."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=GROQ_MAX_TOKENS,
                    temperature=GROQ_TEMPERATURE
                )
                
                enhanced_text = response.choices[0].message.content
                
                # Now use gTTS to convert the enhanced text to speech
                tts = gTTS(text=enhanced_text, lang='en', slow=False)
                
                chunk_path = f"{output_path}_part_{i}.mp3"
                tts.save(chunk_path)
                audio_files.append(chunk_path)
        
        return audio_files
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            logger.error(f"Groq API quota exceeded: {e}")
            return "QUOTA_EXCEEDED"
        elif "insufficient_quota" in error_msg.lower():
            logger.error(f"Groq API insufficient quota: {e}")
            return "QUOTA_EXCEEDED"
        else:
            logger.error(f"Error converting text to speech with Groq: {e}")
            return None

def text_to_speech(text, output_path, model='gtts'):
    """Convert text to speech using the specified model."""
    if model == 'groq':
        return text_to_speech_groq(text, output_path)
    else:  # default to gtts
        return text_to_speech_gtts(text, output_path)
