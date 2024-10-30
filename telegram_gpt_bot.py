import openai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import os

# Настройки
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = "asst_Qt2LiaThdIuNbFFUT4HruyYZ"  # Замените на ID вашего ассистента

openai.api_key = OPENAI_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Я бот с поддержкой заданного ассистента GPT. Задавайте вопросы!')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # Обновленный запрос к OpenAI API
    response = openai.Chat.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message}],
        user=ASSISTANT_ID
    )
    bot_reply = response.choices[0].message['content']

    await update.message.reply_text(bot_reply)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Настройка Webhook с вашим публичным URL
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8443)),
        url_path=TELEGRAM_TOKEN,
        webhook_url=f"https://ximichkabotxxl.onrender.com/{TELEGRAM_TOKEN}"  # Замените на ваш публичный URL на Render
    )



