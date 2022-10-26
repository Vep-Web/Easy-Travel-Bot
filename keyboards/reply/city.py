from config_data.config_site import get_website_request_city
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def city_markup(message: str) -> InlineKeyboardMarkup:
    """
    Функция - inline клавиатуры. Принимает сообщение о поиске города от пользователя и передает
    его для запроса на поиск ближайших локаций.

    :param message: str
    :return: InlineKeyboardMarkup
    """
    cities = get_website_request_city(message)
    destinations = InlineKeyboardMarkup()
    for city in cities:
        destinations.add(InlineKeyboardButton(text=city['city_name'], callback_data=city["destination_id"]))

    return destinations


def count_markup() -> ReplyKeyboardMarkup:
    """
    Функция - reply клавиатуры, которая передает колличество для поиск отелей и фотографий.

    :return: ReplyKeyboardMarkup
    """
    markup_num = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in range(1, 11):
        markup_num.add(str(i))

    return markup_num


def photo_markup() -> ReplyKeyboardMarkup:
    """
    Функция - reply клавиатуры, которая передает клавиатуру с ответом.

    :return: ReplyKeyboardMarkup
    """
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item_yes = KeyboardButton(text='да')
    item_no = KeyboardButton(text='нет')
    markup.add(item_yes, item_no)

    return markup
