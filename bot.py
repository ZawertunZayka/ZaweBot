import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()  # Загружаем токен из .env

BOT_TOKEN = os.getenv('BOT_TOKEN')  # ⚠️ Добавьте в .env!
WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://ваш-сайт.ру')  # Замените на ngrok или хостинг

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🎰 Играть", web_app=WebAppInfo(url=WEBAPP_URL))]]
    await update.message.reply_text(
        "Добро пожаловать в казино!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

if __name__ == '__main__':
    print("Бот запущен!")
    app.run_polling()
