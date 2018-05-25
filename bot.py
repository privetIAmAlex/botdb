from telebot import TeleBot
from worker import Worker

bot = TeleBot("492864827:AAEESNYDf2yaK5bZrFBqbZBnFYatvykT0xY")
_worker = Worker(bot)

@bot.message_handler(content_types=["new_chat_members"])
def handle_new_member(message):
    if message.from_user.id != 497551952:
        _worker.HelloUser(message.chat.id, message.new_chat_member.first_name)
    else:
        bot.delete_message(message.chat.id, message.message_id)

@bot.message_handler(commands=["me"])
def my_stat(message):
    _worker.GetMyStat(message.chat.id, message.message_id, message.from_user.id, message.from_user.first_name)

@bot.message_handler(commands=["top"])
def get_top(message):
    _worker.GetTop(message.chat.id)
 %%%!@$%!^@!$&^%!$@   
##################################################
@bot.message_handler(commands=["удалитьвсёкхерам"])
def gest_top(message):
    bot.send_message(message.chat.id, "Haha, okeeey")
    bot.send_message(message.chat.id, message.from_user.first_name + " запустил самоуничтожение чата!")
    #bot.kick_chat_member()
    ids = [479023442, 567091961, 309231264, 462628534, 539913463, 441587147, 427042660, 420591841, 525431072, 508486363, 417953054, 523121939, 560457928, 530410572, 562794220, 413173722, 343746168, 494203925, 446765362, 443343061, 297042851, 412675829, 506690873, 463978949, 569116397, 510820020, 526734882, 493852801, 537081808, 520753846, 419549168, 458903410, 508057457, 547072323, 492037567, 529164399, 466989094, 486130169, 531172017, 322411488, 523217927, 515068794, 474654036, 528538862, 453389732, 542497357, 380515186, 357612438, 415153796, 534631568, 539400019, 345034231, 471932346, 467224115, 539403685, 477831857, 497618467, 514638149, 448703707, 515515052, 503991169, 314135770, 207384359, 327793280, 495438976, 343092367, 70826021, 551980835, 430402835, 384565834, 611796410, 542268593, 561832945, 447772423, 332700602, 397754091, 425185444, 489935734, 503573429, 37261079, 240532771, 436527567, 416004785, 309231264, 479023442, 506100709, 480632814, 246951417, 526618965, 534732980, 384834009, 461524518, 357454737, 482234239, 392812173, 418338186, 478487810, 547356634, 365110090, 432263005, 418083138, 420029859, 426989133, 585031957, 351456112, 566193604, 483334997, 546959458, 531996262, 326925239, 464123886, 540792613, 548358876, 363436396, 344423049, 434792303, 416318419, 438618244, 438049231]
    bot.send_message(message.chat.id, f"{len(ids)} {min(ids)} {max(ids)}")
    for id in ids:
        user = bot.get_chat_member(-1001137097313, id)
        bot.send_message(message.chat.id, user.user.first_name)

@bot.message_handler(content_types=["photo", "audio", "document", "sticker", "video", "contact"])
def handle_other_types(message):
    _worker.Counter(message.from_user.id)

@bot.message_handler(content_types=["text"])
def handle_message(message):
    if message.chat.id != message.from_user.id:
        _worker.Counter(message.from_user.id)

bot.polling(none_stop=True)

#https://api.telegram.org/bot492864827:AAEESNYDf2yaK5bZrFBqbZBnFYatvykT0xY/getChatMember?chat_id=-1001137097313&user_id=37261079