import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Replace with your bot token
BOT_TOKEN = "7673377030:AAGABRwbjbRrjO0TphZ76vpaf3V8NkZbuqA"
bot = telebot.TeleBot(BOT_TOKEN)

# Dictionary to store chat pairs
active_chats = {}
waiting_users = []

# VIP Members (store in a database for real implementation)
vip_members = set()

# Main Menu Buttons
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🔍 Find Chat"))
    markup.add(KeyboardButton("💎 VIP Membership"), KeyboardButton("❌ Leave Chat"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome to Anonymous Chat Bot!", reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == "🔍 Find Chat")
def find_chat(message):
    user_id = message.chat.id
    if user_id in active_chats:
        bot.send_message(user_id, "You are already in a chat!", reply_markup=main_menu())
        return
    
    if waiting_users:
        partner_id = waiting_users.pop(0)
        active_chats[user_id] = partner_id
        active_chats[partner_id] = user_id
        bot.send_message(user_id, "✅ Connected! Say hi!", reply_markup=main_menu())
        bot.send_message(partner_id, "✅ Connected! Say hi!", reply_markup=main_menu())
    else:
        waiting_users.append(user_id)
        bot.send_message(user_id, "🔄 Waiting for a partner...", reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == "❌ Leave Chat")
def leave_chat(message):
    user_id = message.chat.id
    if user_id in active_chats:
        partner_id = active_chats.pop(user_id)
        active_chats.pop(partner_id, None)
        bot.send_message(user_id, "❌ Chat ended.", reply_markup=main_menu())
        bot.send_message(partner_id, "❌ Chat ended.", reply_markup=main_menu())
    else:
        bot.send_message(user_id, "You're not in a chat!", reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == "💎 VIP Membership")
def vip_info(message):
    bot.send_message(message.chat.id, "VIP members get priority matching! Upgrade now! 💰", reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.chat.id in active_chats)
def chat_handler(message):
    user_id = message.chat.id
    partner_id = active_chats.get(user_id)
    if partner_id:
        bot.send_message(partner_id, message.text)

bot.polling(none_stop=True)
