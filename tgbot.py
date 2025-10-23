import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

with open('story.json', 'r', encoding='utf-8') as f:
    story = json.load(f)

async def start(update: Update, context: CallbackContext):
    context.user_data['current_story'] = 'start'
    await send_story_node(update, 'start', context)

async def handle_message(update: Update, context: CallbackContext):
    user_input = update.message.text.strip()
    current_node_key = context.user_data.get('current_story')

    if not current_node_key:
        await update.message.reply_text('Пожалуйста, начните игру командой /start')
        return

    current_node = story.get(current_node_key)
    if not current_node or ('end' in current_node and current_node['end']):
        await update.message.reply_text('Пожалуйста, начните игру командой /start')
        return

    options = current_node['options']
    matched_option = None
    for key, opt in options.items():
        if user_input == opt['text']:
            matched_option = key
            break

    if matched_option:
        next_node_key = options[matched_option]['next']
        context.user_data['current_story'] = next_node_key
        await send_story_node(update, next_node_key, context)
    else:
        await update.message.reply_text('Пожалуйста, выберите один из вариантов:')
        await send_story_node(update, current_node_key, context)




if __name__ == '__main__':
    app = ApplicationBuilder().token('8408472505:AAHomRYQ-2lEKRvw3RC5oTAwMEjcsDpu99g').build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()
