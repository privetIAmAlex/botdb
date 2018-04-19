from telebot import TeleBot
from worker import Worker

bot = TeleBot("492864827:AAEESNYDf2yaK5bZrFBqbZBnFYatvykT0xY")
_worker = Worker(bot)

@bot.message_handler(content_types=["new_chat_members"])
def handle_new_member(message):
    if message.from_user.id != 497551952:
        _worker.HelloUser(message.chat.id, message.new_chat_member.first_name)

@bot.message_handler(commands=["me"])
def my_stat(message):
    _worker.GetMyStat(message.chat.id, message.message_id, message.from_user.id, message.from_user.first_name)

@bot.message_handler(content_types=["photo", "audio", "document", "sticker", "video", "contact"])
def handle_other_types(message):
    _worker.Counter(message.from_user.id)

@bot.message_handler(content_types=["text"])
def handle_message(message):
    if message.chat.id != message.from_user.id:
        _worker.Counter(message.from_user.id)

bot.polling(none_stop=True)