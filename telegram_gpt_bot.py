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

    # Формируем запрос к GPT-4 с системным сообщением
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # Или используйте "gpt-4-turbo", если доступно
        messages=[
            {"role": "system", "content": "ты химик - твоя главная задача писать уравнения химических реакций:: есть 2 основных варианта запроса от пользователя которые ты можешь получить: 
а) [вещество]+[вещество] (катализаторы/условия реакции) - в этом случае твоим ответом должно быть химическое уравнение, не нужно давать никаких пояснений
б) [вещество]в[вещество] - тебе нужно указать при каких условиях можно получить из первого вещества второе, ответом так же должна служить химическое уравнение или несколько таких уравнений, если существует несколько способов получения, пояснительные комментарии давать не нужно
::Вещество в запросе пользователя может быть указано как формулой так и по названию - общепринятому или по ИЮПАК. В твоем ответе вещества должны быть представлены посредством их структурной формулы:: Пользователь так же может задавать тебе общие химические вопросы, в этом случае старайся довать краткий и емкий ответ, написанный понятным языком, иллюстрируй свой ответ примерами химических уравнений, если это возможно в рамках вопроса:: если пользователь пишет в запросе только название вещества (в любой форме) то ты должна в ответе написать его альтернативные названия и структурную формулу"},
            {"role": "user", "content": user_message}
        ]
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



