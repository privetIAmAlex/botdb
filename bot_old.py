import telebot
from worker import Worker
import time

bot = telebot.TeleBot("492864827:AAFc_KDXUf4-06pZqstFv6HaPO5m5LaruvE")
worker = Worker(bot)

@bot.message_handler(content_types=["audio", "document", "sticker", "video", "contact"])
def other_type_handler(message):
	worker.Counter(message.from_user.id)

@bot.message_handler(content_types=["photo"])
def handle_photo(message):
    worker.Counter(message.from_user.id)
    if message.caption != None and worker.FindBadWord(message.caption):
        try:
            worker.BlockUser(message.from_user.id, message.message_id, message.chat.id, message.from_user.first_name)
        except:
            bot.send_message(message.chat.id, "Так-с, материмся?👮‍♀️", reply_to_message_id=message.message_id)

@bot.message_handler(content_types=["new_chat_members"])
def new_members_handler(message):
    worker.HelloUser(message)

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
        try:
            worker.BlockUser(message.from_user.id, message.message_id, message.chat.id, message.from_user.first_name)
        except:
            bot.send_message(message.chat.id, "Так-с, материмся?👮‍♀️", reply_to_message_id=message.message_id)
    
bot.polling(none_stop=True)