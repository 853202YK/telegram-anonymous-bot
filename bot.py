import os
import logging
import json
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_webhook
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiohttp import web
import aiohttp

# Load environment variables
TOKEN = os.getenv("7673377030:AAGABRwbjbRrjO0TphZ76vpaf3V8NkZbuqA")
PAYPAL_CLIENT_ID = os.getenv("AR2aFhcUCKtnLAJ2RQ7TkA06h1A9TWKgulelPu4kUwoTU4V3jMxiSXEuk31EHEEBOhjiEzLph3iVqC-T")
PAYPAL_CLIENT_SECRET = os.getenv("ELwCRdPPyQr3oWafK1H6US424Jd8x_cJAW8ZSYnTe6MRKlpCOTJUb8AGgwWVXmGThIMZdv7Jxc0q7cfK")
WEBHOOK_URL = "https://mychatbot.up.railway.app/webhook"
WEBHOOK_PATH = "/webhook"
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 8000))
PAYPAL_WEBHOOK_ID = "2N431123CU580432A"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

# Free vs Paid Features
FREE_FEATURES = "\n✅ Anonymous chat\n✅ Random matching\n✅ Limited hidden mode\n✅ Reporting system\n✅ Daily notifications"
PAID_FEATURES = "\n💎 VIP Features:\n✅ Fast Matching\n✅ Gender-Based Search\n✅ Full Hidden Mode\n✅ Ad-Free Experience\n✅ Priority Support\n✅ Payment Integration (Telegram Stars & PayPal)"

# Main Menu Keyboard
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("🔍 Find a partner (/search)"))
main_menu.add(KeyboardButton("👫 Search by gender (VIP) (/pay)"))
main_menu.add(KeyboardButton("💎 Become a VIP (/vip)"))
main_menu.add(KeyboardButton("⚙️ Settings (/settings)"), KeyboardButton("📢 Notifications"))
main_menu.add(KeyboardButton("💰 Payment Support (/paysupport)"))
main_menu.add(KeyboardButton("📜 Rules (/rules)"), KeyboardButton("📖 Terms (/terms)"))
main_menu.add(KeyboardButton("🆔 My ID (/myid)"))

# Start command
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply(f"Welcome to the Anonymous Chat Bot!\nUse the buttons below to navigate.{FREE_FEATURES}\n\nUpgrade to VIP for more benefits: /vip", reply_markup=main_menu)

# VIP Membership
@dp.message_handler(commands=['vip'])
async def vip_command(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Buy VIP (Telegram Stars)", url="https://t.me/yourbot?start=vip"))
    keyboard.add(InlineKeyboardButton("Buy VIP (PayPal)", url="https://yourpaypalpaymentlink.com"))
    await message.reply(f"Become a VIP!\n{PAID_FEATURES}\n\nSelect a payment method below:", reply_markup=keyboard)

# PayPal Webhook Handling
async def handle_paypal_webhook(request):
    data = await request.json()
    logging.info(f"Received PayPal Webhook: {json.dumps(data, indent=2)}")
    
    if data.get("event_type") == "PAYMENT.CAPTURE.COMPLETED":
        user_id = data["resource"]["custom_id"]  # Use custom_id to map user payment
        await bot.send_message(user_id, "✅ Payment received! You are now a VIP user!")
    return web.Response(status=200)

# Webhook setup
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info("Webhook set successfully!")

async def on_shutdown(dp):
    await bot.delete_webhook()
    logging.info("Webhook deleted.")

# Web server for PayPal Webhook
app = web.Application()
app.router.add_post("/webhook", handle_paypal_webhook)

if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
        web_app=app
    )
