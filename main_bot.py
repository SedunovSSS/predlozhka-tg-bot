from telebot import TeleBot, types
from db import *
import json


with open('config.json', 'r') as config_read:
    load_data = json.load(config_read)
    TOKEN = load_data['TOKEN']
    TOKEN_UNBAN = load_data['TOKEN_UNBAN']
    ID = load_data['ID']
    VERSION = load_data['VERSION']
    CHANNEL_NAME = load_data['CHANNEL']

bot = TeleBot(TOKEN)
bot_unban_username = TeleBot(TOKEN_UNBAN).get_me().username
chanell = CHANNEL_NAME

rules = open('rules.txt', 'r', encoding='utf-8').read()

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("✅ Правила ✅")
    markup.add(btn)
    bot.send_message(chat_id=message.chat.id, text=f"Предложка version {VERSION}\nОтправьте мне сообщение", reply_markup=markup)


@bot.message_handler(content_types=['audio', 'photo', 'voice', 'video', 'document',
                'text', 'location', 'contact', 'sticker'])
def all_messages(message):
    try:
        chat_id = message.chat.id
        if is_ban(message.from_user.id):
            bot.send_message(chat_id=message.from_user.id, text=f'❌ Вы забанены! Разбан тут @{bot_unban_username}! ❌')
        else:
            if message.text == "✅ Правила ✅":
                bot.send_message(chat_id=chat_id, text=rules, parse_mode='Markdown')
            else:
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.InlineKeyboardButton(text='❌', callback_data='del')
                btn2 = types.InlineKeyboardButton(text='🚫', callback_data=f'ban-{message.from_user.id}')
                btn3 = types.InlineKeyboardButton(text='✅', callback_data='post')
                btn4 = types.KeyboardButton("✅ Правила ✅")
                markup.row(btn1, btn2, btn3)
                markup1.add(btn4)
                bot.copy_message(ID, chat_id, message.message_id, reply_markup=markup)
                bot.send_message(chat_id=chat_id, text='✅ Ваше Сообщение было отправлено ✅', reply_markup=markup1)
    except:
        bot.send_message(chat_id=message.from_user.id, text='❌ Произошла ошибка! Переотправте сообщение! ❌')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'del':
        bot.delete_message(ID, message_id=call.message.message_id)
        bot.delete_message(ID, message_id=call.message.message_id+1)
    if call.data == 'post':
        bot.forward_message(CHANNEL_NAME, ID, call.message.message_id)
    if str(call.data)[:3] == 'ban':
        ban_id = int(call.data[4:])
        ban_user(ban_id)
        bot.delete_message(ID, message_id=call.message.message_id)
        bot.delete_message(ID, message_id=call.message.message_id+1)
        bot.send_message(chat_id=ban_id, text=f'❌ Вы забанены! Разбан тут @{bot_unban_username}! ❌')
    

bot.infinity_polling()
