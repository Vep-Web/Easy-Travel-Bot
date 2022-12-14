import os
from dotenv import load_dotenv, find_dotenv
from peewee import MySQLDatabase


if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
DEFAULT_COMMANDS = (
    ('start', "Запустить бота."),
    ('help', "Вывести справку."),
    ('lowprice', "Низкая цена."),
    ('highprice', "Высокая цена."),
    ('bestdeal', "Лучший вариант."),
    ('history', "История поиска."),
)

my_db = MySQLDatabase(
    os.getenv("DB_name"),
    user="root",
    password=os.getenv("DB_password"),
    host='localhost',
    port=int(os.getenv("DB_port"))
)
