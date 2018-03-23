import telebot
from worker import Worker
import time
import threading

bot = telebot.TeleBot("492864827:AAFc_KDXUf4-06pZqstFv6HaPO5m5LaruvE")
worker = Worker(bot)
BAN_MESSAGE_ID = []

@bot.message_handler(content_types=["audio", "document", "sticker", "video", "contact"])
def other_type_handler(message):
	worker.Counter(message.from_user.id)

@bot.message_handler(content_types=["new_chat_members"])
def new_members_handler(message):
    worker.HelloUser(message)

@bot.edited_message_handler(func=lambda message: True)
def CheckEdit(message):
    try:
        if message.message_id in BAN_MESSAGE_ID:
            now = time.time()
            if worker.FindBadWord(message.text):
                try:
                    bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=now+3600)
                    bot.send_message(message.chat.id, f"{message.from_user.first_name} заблокирован(а) на 1 час👮‍♀️")
                except:
                    pass
            BAN_MESSAGE_ID.remove(message.message_id)
    except :
        pass

def BlockUser(message):
    t = threading.Timer(30.0, CheckEdit, [message])
    t.start()
    bot.send_message(message.chat.id, "У тебя есть 30 секунд, чтобы удалить или исправить сообщение👮‍♀️", reply_to_message_id=message.message_id)
    BAN_MESSAGE_ID.append(message.message_id)  

@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    worker.Counter(message.from_user.id)
    if message.caption != None and worker.FindBadWord(message.caption):
        try:
            BlockUser(message)
        except:
            bot.send_message(message.chat.id, "😑😑😑", reply_to_message_id=message.message_id)

@bot.message_handler(content_types=["text"])
def handle_message(message):
    if message.chat.id == 497551952:
        day = time.strftime("%w")
        letter = worker.GetStat(day)
        if message.text == "send_stat" and int(day) == 0:
            bot.send_message(-1001137097313, letter, parse_mode="HTML")
        elif message.text == "send_stat_me":
            bot.send_message(497551952, letter, parse_mode="HTML")
            bot.send_message(497551952, day)
            bot.send_message(497551952, str(worker.mess))            
        elif message.text == "unmute":
            bot.restrict_chat_member(-1001137097313, 497551952, until_date=time.time()+35)
        elif message.text == "send_time":
            bot.send_message(497551952, str(time.strftime("%H:%M")))
        return
    worker.Counter(message.from_user.id)
    if worker.FindBadWord(message.text):
        BlockUser(message)

bot.polling(none_stop=True)