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

    # Запрос к OpenAI API с указанием ID ассистента
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message}],
        user=ASSISTANT_ID  # Указание ID ассистента
    )
    bot_reply = response.choices[0].message['content']

    await update.message.reply_text(bot_reply)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск приложения с использованием Webhook или Polling в зависимости от конфигурации
    app.run_polling()

