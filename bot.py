import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# 🔹 Replace with your own bot token
BOT_TOKEN = "7673377030:AAGABRwbjbRrjO0TphZ76vpaf3V8NkZbuqA"
bot = telebot.TeleBot(BOT_TOKEN)

# 🔹 Dictionary to store chat pairs
active_chats = {}
waiting_users = []

# 🔹 VIP Members (You can store in a database later)
vip_members = set()

# 🔹 Main Menu Buttons
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🔍 Find Chat"))
    markup.add(KeyboardButton("🌟 VIP Membership"), KeyboardButton("❌ Leave Chat"))
    return markup

# 🔹 Start Command
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome to Anonymous Chat Bot!", reply_markup=main_menu())

# 🔹 Find a Chat Partner
@bot.message_handler(func=lambda message: message.text == "🔍 Find Chat")
def find_chat(message):
    user_id = message.chat.id

    # If user is already in a chat
    if user_id in active_chats:
        bot.send_message(user_id, "❌ You are already in a chat!")
        return

    # If there is a waiting user, pair them
    if waiting_users:
        partner_id = waiting_users.pop(0)  # Get the first waiting user
        active_chats[user_id] = partner_id
        active_chats[partner_id] = user_id

        bot.send_message(user_id, "✅ Connected! Say hi! 👋")
        bot.send_message(partner_id, "✅ Connected! Say hi! 👋")
    else:
        waiting_users.append(user_id)
        bot.send_message(user_id, "🔄 Waiting for a partner...")

# 🔹 Forward Messages Between Users
@bot.message_handler(func=lambda message: message.chat.id in active_chats)
def forward_message(message):
    user_id = message.chat.id

    if user_id in active_chats:
        partner_id = active_chats[user_id]
        if partner_id in active_chats and active_chats[partner_id] == user_id:
            bot.send_message(partner_id, message.text)
        else:
            bot.send_message(user_id, "❌ Your partner has left the chat.")
            del active_chats[user_id]
    else:
        bot.send_message(user_id, "❌ You are not in a chat!")

# 🔹 Leave Chat
@bot.message_handler(func=lambda message: message.text == "❌ Leave Chat")
def leave_chat(message):
    user_id = message.chat.id

    if user_id in active_chats:
        partner_id = active_chats[user_id]
        bot.send_message(partner_id, "❌ Your partner has left the chat.")
        del active_chats[partner_id]
        del active_chats[user_id]

    elif user_id in waiting_users:
        waiting_users.remove(user_id)

    bot.send_message(user_id, "✅ You left the chat!", reply_markup=main_menu())

# 🔹 Run the bot
print("Bot is running...")
bot.polling()
