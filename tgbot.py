import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

with open('story.json', 'r', encoding='utf-8') as f:
    story = json.load(f)