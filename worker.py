from random import choice
from peewee import PostgresqlDatabase, Model, IntegerField, DoesNotExist
from re import findall
import time
phrases = [
        "Добро пожаловать, {0}!☺️\n\nУ нас культурный чат! Здесь нельзя материться и оскорблять других участников.🚫\nВсе правила ты можешь посмотреть в закреплённом сверху сообщении👆",
        "Приветствую тебя, {0}!✋️\n\nУ нас культурный чат! Здесь нельзя материться и оскорблять других участников.🚫\nВсе правила ты можешь посмотреть в закреплённом сверху сообщении👆",
        "Какие люди! Привет, {0}!😎\n\nПожалуйста, соблюдай правила группы (их ты можешь посмотреть в закреплённом сверху сообщении👆), а то забаню. Шутка🤣",
        "Привет, {0}!🤓\n\nУ нас очень дружелюбный чат, так что не бойся писать, мы не кусаемся!😄 \n\nПравила ты можешь посмотреть в закреплённом сверху сообщении👆"
    ]

db = PostgresqlDatabase(
	database="d8f1mjaq4lsqmk",
    user="torfxnhntooste",
    password="6173a4aac270a1b86399b085f79ed30718af3c63a585597675e62d4366c0ce8d",
    host="ec2-54-163-234-99.compute-1.amazonaws.com",
    port=5432
)

class Person(Model):
    id = IntegerField()
    count_messages = IntegerField()
    class Meta:
        database = db

Person.create_table()

bad_words = []

class Worker():
    def __init__(self, bot):
        self._bot = bot
        with open('badwords.txt', 'r', encoding='cp1251') as file:
            content = file.readlines()
            for word in content:
                bad_words.append(word[:-1])

    def HelloUser(self, chat_id, user_name):
        self._bot.send_message(chat_id, choice(phrases).format(user_name))

    def Counter(self, user_id):
        try:
            p = Person.get(id=user_id)
            p.count_messages += 1
            p.save()
        except DoesNotExist:
            Person.create(id=user_id, count_messages=1).save()

    def GetAsterics(self, x):
        return "*" * (x - 2)

    def FindBadWord(self, chat_id, first_name, text):
        text_array = findall(r"[\w']+", text.lower())
        flag = False
        for word in text_array:
            if word in bad_words:
                new_word = word.replace(word[:-2], self.GetAsterics(len(word)))
                text = text.replace(word, new_word)
                flag=True
        if flag:
            self._bot.send_message(chat_id, f"<b>{first_name}:</b> {text}", parse_mode="HTML")

    def CurrentWord(self, number):                  
        iy = ['11', '12', '13', '14', '5', '6', '7', '8', '9', '0']
        if number.endswith('1'):
            return "сообщение"
        elif number.endswith('2') or number.endswith('3') or number.endswith('4'):
            return "сообщения"
        else:
            for i in range(len(iy)):
                if iy[i] in number:
                    return "сообщений"

    def AdminPanel(self, command):
        print("Зашёл в метод")
        stat = ""
        iter = 0
        for one in Person.select().order_by(Person.count_messages.desc()).limit(10):
            print("В цикле")
            try:
                _user = self._bot.get_chat_member(-1001137097313, one.id)
                name = "@" + _user.user.username if _user.user.username != None else _user.user.first_name
                if iter == 0: 
                    stat += f"🥇{name} - {one.count_messages}\n"
                    iter += 1
                elif iter == 1:
                    stat += f"🥈{name} - {one.count_messages}\n"
                    iter += 1
                elif iter == 2:
                    stat += f"🥉{name} - {one.count_messages}\n"
                    iter += 1
                else:
                    stat += f"     {name} - {one.count_messages}\n"
            except Exception:
                stat += f"~outgoing - {one.count_messages}\n"
                iter += 1
        print("Вышел из цикла")
        total = 0
        for i in Person.select():
            total += i.count_messages
        letter = "Вот и подошла к концу ещё одна неделя! И вот вам немного статистики:\n\n<i>Самые активные участники:</i>\n{}\nА всего было напечатано <b>{}</b> {}!\n\nУдачи в наступающей неделе!😉".format(stat, total, self.CurrentWord(str(total)))
        
        if command == "send_stat_me":
            print("Принял команду")
            self._bot.send_message(497551952, letter, parse_mode="HTML")
        elif command == "send_stat":
            if time.strftime("%w") == 0:
                self._bot.send_message(-1001137097313, letter, parse_mode="HTML")            