from telebot import TeleBot, types
from db import *
import json

with open('config.json', 'r') as config_read:
    load_data = json.load(config_read)
    TOKEN = load_data['TOKEN_UNBAN']
    ID = load_data['ID']
    VERSION = load_data['VERSION']

bot = TeleBot(TOKEN)

@bot.message_handler(content_types=['text'])
def start(message):
    chat_id = message.from_user.id
    if is_ban(chat_id):
        msg = bot.send_message(chat_id=message.from_user.id, text='Напишите извинение перед админом: ')
        bot.register_next_step_handler(msg, send_unban)
    else:
        bot.send_message(chat_id=message.from_user.id, text='✅ Вы пока не забанены ✅')


@bot.message_handler(content_types=['photo', 'voice', 'video', 'text'])
def send_unban(message):
    chat_id = message.chat.id
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='❌', callback_data=f'not-{message.from_user.id}')
    btn2 = types.InlineKeyboardButton(text='✅', callback_data=f'unban-{message.from_user.id}')
    markup.row(btn1, btn2)
    bot.copy_message(ID, chat_id, message.message_id, reply_markup=markup)
    msg = bot.send_message(chat_id=chat_id, text='✅ Ваше Извинение было отправлено ✅')
    bot.register_next_step_handler(msg, start)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if str(call.data)[:5] == 'unban':
        ban_id = int(call.data[6:])
        unban_user(ban_id)
        bot.send_message(chat_id=ban_id, text=f'✅ Вы Разбанены ✅')
        bot.delete_message(ID, message_id=call.message.message_id)
        bot.delete_message(ID, message_id=call.message.message_id-1)
    if str(call.data)[:3]  == 'not':
        ban_id = int(call.data[4:])
        bot.send_message(chat_id=ban_id, text=f'❌ Админ решил вас не разбанивать ❌')
        bot.delete_message(ID, message_id=call.message.message_id)
        bot.delete_message(ID, message_id=call.message.message_id-1)


bot.infinity_polling()