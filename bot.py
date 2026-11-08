import os
import logging
import threading
import requests
from flask import Flask
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# রেন্ডারের পোর্ট বাইন্ডিংয়ের জন্য ফ্লাস্ক সার্ভার
app = Flask(__name__)

@app.route('/')
def home():
    return "NP Network Bot is Active and Running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# লোগিং সেটআপ
logging.basicConfig(level=logging.INFO)

API_TOKEN = "NP-6HXU732PNEATGVFM"
BASE_URL = "https://www.npnetworkbd.com/api/user"
TELEGRAM_BOT_TOKEN = "9168159119:AAFmg9tj8WKpvJ2mswXW5ipQjf3rQb0eZ7o"

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("NP Network OTP Bot is active and running successfully!")

@dp.message_handler(commands=['status'])
async def check_status(message: types.Message):
    try:
        headers = {'mauthapi': API_TOKEN}
        res = requests.get(f"{BASE_URL}/success-otp", headers=headers, timeout=10)
        if res.status_code == 200:
            await message.reply("API Connection Successful! Backend is operational.")
        else:
            await message.reply(f"API returned status code: {res.status_code}")
    except Exception as e:
        await message.reply(f"API Connection Error: {str(e)}")

if __name__ == '__main__':
    # ব্যাকগ্রাউন্ডে ফ্লাস্ক সার্ভার চালু করা যাতে রেন্ডার পোর্ট পেয়ে যায়
    web_thread = threading.Thread(target=run_web)
    web_thread.daemon = True
    web_thread.start()

    logging.info("Starting Python Backend Bot for NP Network...")
    executor.start_polling(dp, skip_updates=True)
