from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):
    cities = State()
    count_hotels = State()
    count_photo = State()
    photo = State()
