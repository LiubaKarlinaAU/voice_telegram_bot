"""
Main Telegram PDF to MP3 Bot
"""
import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from config import BOT_TOKEN
from handlers import (
    start, help_command, echo_command, pdf2mp3_command, extract_text_command,
    tts_model_command, current_model_command, button_callback,
    handle_document, handle_message, error_handler
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
    """Start the bot."""
    # Check if running on Railway (for health checks)
    if os.getenv('RAILWAY_ENVIRONMENT'):
        print("🚀 Running on Railway cloud platform")
        print(f"Environment: {os.getenv('RAILWAY_ENVIRONMENT')}")
    
    # Validate environment variables
    if not BOT_TOKEN:
        print("❌ ERROR: BOT_TOKEN not found!")
        print("Please set BOT_TOKEN in Railway environment variables")
        return
    
    print(f"✅ Bot token found: {BOT_TOKEN[:10]}...")
    
    # Check for GROQ_TOKEN (optional)
    from config import GROQ_TOKEN
    if GROQ_TOKEN:
        print(f"✅ Groq token found: {GROQ_TOKEN[:10]}...")
    else:
        print("⚠️  GROQ_TOKEN not found - Groq features will be disabled")
    
    # Create the Updater
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("echo", echo_command))
    dispatcher.add_handler(CommandHandler("pdf2mp3", pdf2mp3_command))
    dispatcher.add_handler(CommandHandler("extract", extract_text_command))
    dispatcher.add_handler(CommandHandler("tts_model", tts_model_command))
    dispatcher.add_handler(CommandHandler("current_model", current_model_command))
    dispatcher.add_handler(CallbackQueryHandler(button_callback))
    dispatcher.add_handler(MessageHandler(Filters.document, handle_document))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Register error handler
    dispatcher.add_error_handler(error_handler)

    # Start the bot
    print("Bot is starting...")
    print("Press Ctrl+C to stop the bot")
    
    try:
        # Start the Bot with connection retry logic
        print("🔄 Starting polling...")
        
        # Test connection first
        try:
            bot_info = updater.bot.get_me()
            print(f"✅ Connected to Telegram API successfully!")
            print(f"🤖 Bot username: @{bot_info.username}")
            print(f"📝 Bot name: {bot_info.first_name}")
        except Exception as conn_e:
            print(f"❌ Failed to connect to Telegram API: {conn_e}")
            logger.error(f"Telegram API connection failed: {conn_e}")
            return
        
        # Start polling with error handling
        updater.start_polling(
            drop_pending_updates=True,  # Drop any pending updates on restart
            allowed_updates=['message', 'callback_query']  # Only handle these update types
        )
        print("✅ Bot is now running and polling for updates!")

        # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT
        updater.idle()
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        logger.error(f"Bot startup error: {e}")
        raise

if __name__ == '__main__':
    main()
