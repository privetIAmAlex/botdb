from random import choice
from peewee import PostgresqlDatabase, Model, IntegerField, DoesNotExist
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
    user_id = IntegerField()
    count_messages = IntegerField()
    class Meta:
        database = db

Person.create_table()

class Worker():
    def __init__(self, bot):
        self._bot = bot

    def HelloUser(self, chat_id, user_name):
        self._bot.send_message(chat_id, choice(phrases).format(user_name))

    def Counter(self, _user_id):
        try:
            p = Person.get(user_id=_user_id)
            p.count_messages += 1
            p.save()
        except DoesNotExist:
            Person.create(user_id=_user_id, count_messages=1).save()

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

    def GetMyStat(self, _chat_id, _message_id, _user_id, _user_first_name):
        letter = ""
        try:
            p = Person.get(user_id=_user_id)
            letter = "{} написал(а) <b>{}</b> {}👍".format(_user_first_name, p.count_messages, self.CurrentWord(str(p.count_messages)))
        except DoesNotExist:
            letter = "Ты пока ещё не написал(а) ни одного сообщения😑"
        # try:
        #     self._bot.delete_message(_chat_id, _message_id)
        # except:pass
        self._bot.send_message(_chat_id, letter, parse_mode="HTML")

    def GetTop(self, chat_id):
        stat = ""
        iter = 0
        for one in Person.select().order_by(Person.count_messages.desc()):
            if iter > 10 : break
            try:
                _user = self._bot.get_chat_member(-1001137097313, one.user_id) #chat_id
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
                #stat += f"~~~ - {one.count_messages}\n"
                #iter += 1
                pass

        letter = "Топ-10 участников группы:\n\n{}".format(stat)
        self._bot.send_message(chat_id, letter)