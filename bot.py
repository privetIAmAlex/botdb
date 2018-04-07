from telebot import TeleBot
from worker import Worker

bot = TeleBot("492864827:AAFc_KDXUf4-06pZqstFv6HaPO5m5LaruvE")
_worker = Worker(bot)

@bot.message_handler(content_types=["new_chat_member"])
def handle_new_member(message):
    _worker.HelloUser(message.chat.id, message.from_user.first_name)

@bot.message_handler(content_types=["photo", "audio", "document", "sticker", "video", "contact"])
def handle_other_types(message):
    _worker.Counter(message.from_user.id)

@bot.message_handler(content_types=["text"])
def handle_message(message):
    if message.chat.id == 497551952:
        _worker.AdminPanel(message.text)
        return
    _worker.FindBadWord(message.chat.id, message.from_user.first_name, message.text)

bot.polling(none_stop=True)