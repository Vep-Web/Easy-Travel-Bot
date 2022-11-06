from states.contact_info import User
from loader import bot
from config_data.config import my_db
import peewee
import telebot


class BaseModel(peewee.Model):
    class Meta:
        database = config.my_db


class User_Data(BaseModel):
    user_telegram_id = peewee.IntegerField()
    user_command = peewee.CharField()
    user_time_request = peewee.CharField()
    user_hotels_list = peewee.CharField()


def create_db() -> None:
    """
    Функция создает базу данных, если она отсутствует.
    :return:
    """
    try:
        my_db.connect()
        User_Data.create_table()
    except peewee.InternalError as px:
        print(str(px))


def add_user_data(user_telegram_id, command, request_time, text_for_database) -> None:
    """
    Функция создает запись в базе данных.
    :param user_telegram_id:
    :param command:
    :param request_time:
    :param text_for_database:
    :return:
    """

    with my_db:
        User_Data.create(user_telegram_id=user_telegram_id,
                         user_command=command,
                         user_time_request=request_time,
                         user_hotels_list=text_for_database
                         )


def to_use_literals(string: str) -> str:
    """
    Функция принимает значение 'название отелей' из базы данных и в этом значении заменяет символ ; на литерал
    :param string:
    :return: string
    """
    return string.replace(';', '\n')


def show_history(message: telebot.types.Message) -> None:
    """
    Функция, которая отправляет пользователю историю запросов.
    :param message:
    :return: None
    """

    user = User.get_user(message.from_user.id)
    with my_db:
        for data in User_Data.select().where(User_Data.user_telegram_id == user.user_id):
            history_to_show = f"Команда: {data.user_command}\n" \
                              f"Дата и время обращения: {data.user_time_request}\n" \
                              f"Список найденных отелей:\n{to_use_literals(data.user_hotels_list)}"
            bot.send_message(user.user_id, history_to_show)