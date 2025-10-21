"""
Bot command and message handlers.
"""
import os
import tempfile
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from utils import extract_text_from_pdf, text_to_speech
from config import DEFAULT_TTS_MODEL, AVAILABLE_MODELS

logger = logging.getLogger(__name__)

# Global variable to store TTS model preference
user_tts_preferences = {}  # Store user preferences: {user_id: 'gtts' or 'groq'}

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    welcome_message = (
        f"Hi {user.first_name}!\n\n"
        f"I'm a simple Telegram bot with PDF to MP3 conversion!\n\n"
        f"🤖 **PDF to MP3 Bot**\n\n"
        f"**Available Commands:**\n"
        f"• /start - Show this welcome message\n"
        f"• /help - Show help information\n"
        f"• /echo <text> - Echo back your message\n"
        f"• /pdf2mp3 - Convert PDF to MP3 audio\n"
        f"• /extract - Extract text from PDF only\n"
        f"• /tts_model - Choose TTS model\n"
        f"• /current_model - Show current TTS model\n\n"
        f"**How to use:**\n"
        f"1️⃣ Choose your TTS model below\n"
        f"2️⃣ Send me a PDF file\n"
        f"3️⃣ Get your MP3 audio!\n\n"
        f"Choose your TTS model:"
    )
    # Create inline keyboard for TTS model selection
    keyboard = [
        [
            InlineKeyboardButton("🇺🇸 Google TTS (Free)", callback_data="tts_gtts"),
            InlineKeyboardButton("🤖 Groq AI (Enhanced)", callback_data="tts_groq")
        ],
        [
            InlineKeyboardButton("ℹ️ Model Info", callback_data="model_info"),
            InlineKeyboardButton("❓ Help", callback_data="help_info")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode='Markdown')

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
**PDF to MP3 Bot Help**

**Commands:**
• /start - Show welcome message
• /help - Show help information
• /echo <text> - Echo back your message
• /pdf2mp3 - Convert PDF to MP3 audio
• /extract - Extract text from PDF only
• /tts_model - Choose TTS model
• /current_model - Show current TTS model

**Features:**
- Responds to any text message
- Simple command handling
- PDF to MP3 conversion with multiple TTS models
- Text extraction from PDFs
- Basic logging

**Available TTS Models:**

🇺🇸 **Google TTS (gTTS)**
• ✅ Free and fast
• ✅ Supports multiple languages (Russian, English, etc.)
• ✅ Output in original language
• ✅ No API costs

🤖 **Groq AI (llama-3.1-8b-instant)**
• ✅ AI-enhanced text processing
• ✅ Can parse Russian text → English output
• ✅ Better speech quality
• ⚠️ Requires API credits

**How to use PDF to MP3:**
1. Choose your TTS model: /tts_model gtts or /tts_model groq
2. Send a PDF file to the bot
3. The bot will extract text and convert to MP3
4. You'll receive the audio file(s)

**If you get quota errors:**
- The bot will still extract and send you the text
- You can use /extract command for text-only extraction
- Try switching models with /tts_model command

Just send me any message or PDF file!
    """
    update.message.reply_text(help_text, parse_mode='Markdown')

def echo_command(update: Update, context: CallbackContext) -> None:
    """Echo the user message when /echo command is used."""
    if context.args:
        message = ' '.join(context.args)
        update.message.reply_text(f"Echo: {message}")
    else:
        update.message.reply_text("Please provide a message to echo. Usage: /echo <your message>")

def pdf2mp3_command(update: Update, context: CallbackContext) -> None:
    """Handle PDF to MP3 conversion command."""
    update.message.reply_text(
        "Please send me a PDF file and I'll convert it to MP3 audio!\n\n"
        "Just upload the PDF file and I'll process it automatically using your selected TTS model.\n\n"
        "Note: If you encounter quota issues, the bot will still extract and send you the text content."
    )

def extract_text_command(update: Update, context: CallbackContext) -> None:
    """Handle text extraction command."""
    update.message.reply_text(
        "Please send me a PDF file and I'll extract the text for you!\n\n"
        "This command only extracts text without converting to audio."
    )

def tts_model_command(update: Update, context: CallbackContext) -> None:
    """Handle TTS model selection command."""
    user_id = update.effective_user.id
    
    if not context.args:
        current_model = user_tts_preferences.get(user_id, DEFAULT_TTS_MODEL)
        model_info = AVAILABLE_MODELS[current_model]
        update.message.reply_text(
            f"Current TTS model: {current_model.upper()}\n\n"
            f"Usage: /tts_model <gtts|groq>\n\n"
            f"Available models:\n"
            f"• gtts - Google Text-to-Speech (free, fast)\n"
            f"• groq - Groq with llama-3.1-8b-instant (enhanced with AI)"
        )
        return
    
    model = context.args[0].lower()
    if model in ['gtts', 'groq']:
        user_tts_preferences[user_id] = model
        model_info = AVAILABLE_MODELS[model]
        update.message.reply_text(
            f"✅ TTS model set to: {model.upper()}\n\n"
            f"Your PDF to MP3 conversions will now use {model_info['name']}."
        )
    else:
        update.message.reply_text(
            "❌ Invalid model. Please use:\n"
            "• /tts_model gtts - for Google Text-to-Speech\n"
            "• /tts_model groq - for Groq with llama-3.1-8b-instant"
        )

def current_model_command(update: Update, context: CallbackContext) -> None:
    """Show current TTS model."""
    user_id = update.effective_user.id
    current_model = user_tts_preferences.get(user_id, DEFAULT_TTS_MODEL)
    model_info = AVAILABLE_MODELS[current_model]
    
    update.message.reply_text(
        f"Current TTS model: {current_model.upper()}\n"
        f"Description: {model_info['emoji']} {model_info['name']} - {model_info['description']}\n\n"
        f"Use /tts_model to change your model."
    )

def button_callback(update: Update, context: CallbackContext) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    query.answer()
    
    user_id = update.effective_user.id
    
    if query.data == "tts_gtts":
        user_tts_preferences[user_id] = 'gtts'
        model_info = AVAILABLE_MODELS['gtts']
        features_text = "\n".join([f"• {feature}" for feature in model_info['features']])
        query.edit_message_text(
            f"✅ **{model_info['name']} Selected!**\n\n"
            f"{model_info['emoji']} **{model_info['name']}**\n"
            f"{features_text}\n\n"
            f"Send me a PDF file to convert to MP3!",
            parse_mode='Markdown'
        )
    elif query.data == "tts_groq":
        user_tts_preferences[user_id] = 'groq'
        model_info = AVAILABLE_MODELS['groq']
        features_text = "\n".join([f"• {feature}" for feature in model_info['features']])
        query.edit_message_text(
            f"✅ **{model_info['name']} Selected!**\n\n"
            f"{model_info['emoji']} **{model_info['name']} (llama-3.1-8b-instant)**\n"
            f"{features_text}\n\n"
            f"Send me a PDF file to convert to MP3!",
            parse_mode='Markdown'
        )
    elif query.data == "model_info":
        gtts_info = AVAILABLE_MODELS['gtts']
        groq_info = AVAILABLE_MODELS['groq']
        
        gtts_features = "\n".join([f"• ✅ {feature}" for feature in gtts_info['features']])
        groq_features = "\n".join([f"• ✅ {feature}" for feature in groq_info['features']])
        
        query.edit_message_text(
            f"**TTS Model Information**\n\n"
            f"{gtts_info['emoji']} **{gtts_info['name']} (gTTS)**\n"
            f"{gtts_features}\n\n"
            f"{groq_info['emoji']} **{groq_info['name']} (llama-3.1-8b-instant)**\n"
            f"{groq_features}\n\n"
            f"Choose your preferred model:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🇺🇸 Google TTS", callback_data="tts_gtts"),
                 InlineKeyboardButton("🤖 Groq AI", callback_data="tts_groq")],
                [InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]
            ]),
            parse_mode='Markdown'
        )
    elif query.data == "help_info":
        query.edit_message_text(
            "**Bot Help**\n\n"
            "**Commands:**\n"
            "• /start - Show welcome message\n"
            "• /help - Show help information\n"
            "• /pdf2mp3 - Convert PDF to MP3\n"
            "• /extract - Extract text only\n"
            "• /tts_model - Choose TTS model\n"
            "• /current_model - Show current model\n\n"
            "**How to use:**\n"
            "1️⃣ Choose your TTS model\n"
            "2️⃣ Send me a PDF file\n"
            "3️⃣ Get your MP3 audio!\n\n"
            "Choose your TTS model:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🇺🇸 Google TTS", callback_data="tts_gtts"),
                 InlineKeyboardButton("🤖 Groq AI", callback_data="tts_groq")],
                [InlineKeyboardButton("ℹ️ Model Info", callback_data="model_info"),
                 InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]
            ]),
            parse_mode='Markdown'
        )
    elif query.data == "back_to_start":
        # Reset to start message
        welcome_message = (
            f"Hi {update.effective_user.first_name}!\n\n"
            f"I'm a simple Telegram bot with PDF to MP3 conversion!\n\n"
            f"🤖 **PDF to MP3 Bot**\n\n"
            f"**Available Commands:**\n"
            f"• /start - Show this welcome message\n"
            f"• /help - Show help information\n"
            f"• /echo <text> - Echo back your message\n"
            f"• /pdf2mp3 - Convert PDF to MP3 audio\n"
            f"• /extract - Extract text from PDF only\n"
            f"• /tts_model - Choose TTS model\n"
            f"• /current_model - Show current TTS model\n\n"
            f"**How to use:**\n"
            f"1️⃣ Choose your TTS model below\n"
            f"2️⃣ Send me a PDF file\n"
            f"3️⃣ Get your MP3 audio!\n\n"
            f"Choose your TTS model:"
        )
        keyboard = [
            [
                InlineKeyboardButton("🇺🇸 Google TTS (Free)", callback_data="tts_gtts"),
                InlineKeyboardButton("🤖 Groq AI (Enhanced)", callback_data="tts_groq")
            ],
            [
                InlineKeyboardButton("ℹ️ Model Info", callback_data="model_info"),
                InlineKeyboardButton("❓ Help", callback_data="help_info")
            ]
        ]
        query.edit_message_text(
            welcome_message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

def handle_document(update: Update, context: CallbackContext) -> None:
    """Handle PDF document uploads."""
    document = update.message.document
    
    # Check if it's a PDF file
    if document.mime_type == 'application/pdf':
        update.message.reply_text("PDF received! Processing...")
        
        try:
            # Download the PDF file
            file = context.bot.get_file(document.file_id)
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
                file.download(temp_pdf.name)
                pdf_path = temp_pdf.name
            
            # Extract text from PDF
            text = extract_text_from_pdf(pdf_path)
            
            if not text or not text.strip():
                update.message.reply_text("Sorry, I couldn't extract any text from this PDF. The PDF might be image-based or corrupted.")
                os.unlink(pdf_path)
                return
            
            # Create temporary directory for audio files
            with tempfile.TemporaryDirectory() as temp_dir:
                audio_path = os.path.join(temp_dir, "audio")
                
                # Get user's TTS model preference
                user_id = update.effective_user.id
                selected_model = user_tts_preferences.get(user_id, DEFAULT_TTS_MODEL)
                
                # Convert text to speech using selected model
                audio_files = text_to_speech(text, audio_path, model=selected_model)
                
                if audio_files == "QUOTA_EXCEEDED":
                    model_name = selected_model.upper()
                    if selected_model == 'groq':
                        error_msg = (
                            "❌ Groq API quota exceeded!\n\n"
                            "Your Groq API has rate limits or quota issues.\n\n"
                            "This might be due to:\n"
                            "1. Too many requests in a short time\n"
                            "2. API quota exceeded\n"
                            "3. Network connectivity issues\n\n"
                            "Please try again later or switch to gTTS model using /tts_model gtts\n\n"
                            f"📄 Extracted text:\n{text[:1000]}{'...' if len(text) > 1000 else ''}"
                        )
                    else:
                        error_msg = (
                            "❌ gTTS API quota exceeded!\n\n"
                            "Google Text-to-Speech service has rate limits.\n\n"
                            "This might be due to:\n"
                            "1. Too many requests in a short time\n"
                            "2. Network connectivity issues\n"
                            "3. Google service limitations\n\n"
                            "Please try again later or use the extracted text below:\n\n"
                            f"📄 Extracted text:\n{text[:1000]}{'...' if len(text) > 1000 else ''}"
                        )
                    update.message.reply_text(error_msg)
                elif audio_files:
                    # Send audio files
                    model_name = selected_model.upper()
                    for audio_file in audio_files:
                        with open(audio_file, 'rb') as f:
                            update.message.reply_audio(
                                audio=f,
                                title=f"PDF Audio - Part {audio_files.index(audio_file) + 1}",
                                performer=model_name
                            )
                    
                    update.message.reply_text(f"Successfully converted PDF to MP3 using {model_name}! Sent {len(audio_files)} audio file(s).")
                else:
                    update.message.reply_text("Sorry, there was an error converting the text to speech.")
            
            # Clean up PDF file
            os.unlink(pdf_path)
            
        except Exception as e:
            logger.error(f"Error processing PDF: {e}")
            update.message.reply_text("Sorry, there was an error processing your PDF file.")
    else:
        update.message.reply_text("Please send a PDF file for conversion to MP3.")

def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle regular text messages."""
    user_message = update.message.text
    user = update.effective_user
    
    # Simple response logic
    if user_message.lower() in ['hello', 'hi', 'hey']:
        response = f"Hello {user.first_name}!"
    elif user_message.lower() in ['bye', 'goodbye', 'see you']:
        response = f"Goodbye {user.first_name}!"
    elif '?' in user_message:
        response = "That's an interesting question!"
    else:
        response = f"You said: '{user_message}'\n\nI'm a simple bot, but I'm listening!"
    
    update.message.reply_text(response)

def error_handler(update: Update, context: CallbackContext) -> None:
    """Log the error and send a telegram message to notify the developer."""
    logger.warning(f'Update {update} caused error {context.error}')
