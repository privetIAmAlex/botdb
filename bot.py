import telebot
from worker import Worker
import time

bot = telebot.TeleBot("492864827:AAFc_KDXUf4-06pZqstFv6HaPO5m5LaruvE")
worker = Worker(bot)

@bot.message_handler(content_types=["new_chat_members"])
def new_members_handler(message):
    worker.HelloUser(message)

@bot.message_handler(content_types=["text"])
def handle_message(message):
    if message.chat.id == 497551952:
        if message.text == "send_stat":
            day = time.strftime("%w")
            letter = worker.GetStat(day)
            if day == 6:
                bot.send_message(-1001137097313, letter, parse_mode="HTML")
            else:
                bot.send_message(497551952, letter, parse_mode="HTML")
        elif message.text == "unmute":
            bot.restrict_chat_member(-1001137097313, 497551952, until_date=time.time()+35)
        return
    worker.Counter(message.from_user.id)
    if worker.FindBadWord(message.text):
        try:
            worker.BlockUser(message.from_user.id, message.message_id, message.chat.id, message.from_user.first_name)
        except:
            bot.send_message(message.chat.id, "Так-с, материмся?👮‍♀️", reply_to_message_id=message.message_id)
    
bot.polling(none_stop=True)