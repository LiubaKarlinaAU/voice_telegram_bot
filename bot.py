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
    
    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
