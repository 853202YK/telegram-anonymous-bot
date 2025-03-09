import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor

TOKEN = "7673377030:AAGABRwbjbRrjO0TphZ76vpaf3V8NkZbuqA"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

users = {}  # Stores user states
waiting = []  # Users waiting for a chat

@dp.message_handler(commands=['start'])
async def start(message: Message):
    users[message.chat.id] = None  # User starts with no partner
    await message.answer("Welcome to Anonymous Chat Bot!\nUse /search to find a chat partner.")

@dp.message_handler(commands=['search'])
async def search(message: Message):
    user_id = message.chat.id
    if users[user_id]:
        await message.answer("You are already in a chat. Use /leave first.")
        return
    
    if waiting:
        partner_id = waiting.pop(0)
        users[user_id] = partner_id
        users[partner_id] = user_id
        await bot.send_message(user_id, "Connected! Say hi!")
        await bot.send_message(partner_id, "Connected! Say hi!")
    else:
        waiting.append(user_id)
        await message.answer("Waiting for a partner...")

@dp.message_handler(commands=['leave'])
async def leave(message: Message):
    user_id = message.chat.id
    partner_id = users.get(user_id)
    
    if partner_id:
        await bot.send_message(partner_id, "Your partner has left the chat.")
        users[partner_id] = None
    
    users[user_id] = None
    await message.answer("You left the chat. Use /search to find a new partner.")

@dp.message_handler()
async def chat(message: Message):
    user_id = message.chat.id
    partner_id = users.get(user_id)
    
    if partner_id:
        await bot.send_message(partner_id, message.text)
    else:
        await message.answer("You're not in a chat. Use /search to find a partner.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
