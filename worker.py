import random
from peewee import *
import time

db = SqliteDatabase("Database.sqlite")

class Person(Model):
    user_id = IntegerField()
    count_messages = IntegerField()
    ban_id = IntegerField(default=0)
    class Meta:
        database = db

class Record(Model):
    total_counts = IntegerField()
    class Meta:
        database = db

Person.create_table()
Record.create_table()

class Worker:

    BOT = None
    bad_words = []
    phrases = [
        "Добро пожаловать, {0}!☺️\n\nУ нас культурный чат! Здесь нельзя материться и оскорблять других участников.🚫\nВсе правила ты можешь посмотреть в закреплённом сверху сообщении👆\n\nДавай познакомимся? Расскажи немного о себе!🤗",
        "Приветствую тебя, {0}!✋️\n\nУ нас культурный чат! Здесь нельзя материться и оскорблять других участников.🚫\nВсе правила ты можешь посмотреть в закреплённом сверху сообщении👆\n\nРасскажешь что-нибудь о себе?😊",
        "Какие люди! Привет, {0}!😎\n\nПожалуйста, соблюдай правила группы, а то забаню. Шутка🤣\nВсе правила ты можешь посмотреть в закреплённом сверху сообщении👆\n\nДавай познакомимся? Расскажи что-нибудь о себе🤗",
        "Привет, {0}!🤓\n\nУ нас очень дружелюбный чат, так что не бойся писать, мы не кусаемся!😄 Только не матерись, пожалуйста😉\n\nВсе правила ты можешь посмотреть в закреплённом сверху сообщении👆"
    ]

    def __init__(self, _bot):
        self.BOT = _bot
        with open('badwords.txt', 'r', encoding='cp1251') as f:  
            content = f.readlines()
            for word in content:
                self.bad_words.append(word[:-1])

    def HelloUser(self, _message):
        user_name = _message.new_chat_member.first_name
        self.BOT.send_message(_message.chat.id, random.choice(self.phrases).format(user_name))

    def Counter(self, user_id):
        try:
            a = Person.get(Person.user_id == user_id)
            a.count_messages += 1
            a.save()
        except DoesNotExist:
            Person.create(user_id=user_id, count_messages = 1, ban_id=0)

    def FindBadWord(self, text):
        text = text.lower()
        for word in self.bad_words:
            if word in text:
                return True
        return False

    def BlockUser(self, user_id, message_id, chat_id, first_name):
        a = Person.get(Person.user_id == user_id)
        a.ban_id = a.ban_id + 1
        a.save()
        now = time.time()
        if a.ban_id >= 3:
            self.BOT.restrict_chat_member(chat_id, user_id, until_date=now+3600)
            self.BOT.send_message(chat_id, "<b>{} заблокирован(а) на 1 час</b>\n\n{}, у нас нельзя материться!\nВ следующий раз наказание будет строже!".format(first_name, first_name), parse_mode="html")
        elif a.ban_id == 2:
            self.BOT.restrict_chat_member(chat_id, user_id, until_date=now+300)
            self.BOT.send_message(chat_id, "<b>{} заблокирован(а) на 5 минут</b>\n\n{}, у нас нельзя материться!\nВ следующий раз наказание будет строже!".format(first_name, first_name), parse_mode="html")
        else:
            self.BOT.restrict_chat_member(chat_id, user_id, until_date=now+60)
            self.BOT.send_message(chat_id, "<b>{} заблокирован(а) на 1 минуту</b>\n\n{}, у нас нельзя материться!\nВ следующий раз наказание будет строже!".format(first_name, first_name), parse_mode="html")
        self.BOT.delete_message(chat_id, message_id)

    def CurrentWord(self, number):
        iy = ['11', '12', '13', '14', '5', '6', '7', '8', '9', '0']
        for i in range(len(iy)):
            if iy[i] in number:
                return "сообщений"          
        if number.endswith('1'):
            return "сообщение"
        elif number.endswith('2') or number.endswith('3') or number.endswith('4'):
            return "сообщения"
        else:
            return "сообщ."

    def GetStat(self, _day):
        stat = ""
        iter = 0
        for one in Person.select().order_by(Person.count_messages.desc()).limit(10):
            user = self.BOT.get_chat_member(-1001137097313, one.user_id)
            if iter == 0: 
                stat += f"🥇{user.first_name} {one.count_messages}\n"
                iter += 1
            elif iter == 1:
                stat += f"🥈{user.first_name} {one.count_messages}\n"
                iter += 1
            elif iter == 2:
                stat += f"🥉{user.first_name} {one.count_messages}\n"
                iter += 1
            else:
                stat += f"       {user.first_name} {one.count_messages}\n"
        total = 0
        for i in Person.select().order_by(Person.count_messages):
            total += i.count_messages

        insert = ""
        if _day != 6:            
            for rec in Record.select().order_by(Record.total_counts.desc()).limit(1):
                if total > rec.total_counts:
                    insert = "Мы поставили новый рекорд!🎉"
                    a = Record.create(total_counts=total)
                    rec.delete_instance()
                    a.save()                    
                else:
                    res = rec.total_counts - total
                    insert = f"Ещё бы <b>{res}</b> {self.CurrentWord(str(res))} и мы побили бы прошлый рекорд😌"
        letter = "Вот и подошла к концу ещё одна неделя! И вот вам немного статистики:\n\n<i>Самые активные участники:</i>\n{}\nА всего было напечатано <b>{}</b> {}!\n{}\n\nУдачи в наступающей неделе!😉".format(stat, total, self.CurrentWord(str(total)), insert)
        return letter

        ##