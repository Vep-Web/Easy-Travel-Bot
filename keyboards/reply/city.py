from config_data.config_site import get_website_request_city
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def city_markup(message):
    cities = get_website_request_city(message)
    destinations = InlineKeyboardMarkup()
    for city in cities:
        destinations.add(InlineKeyboardButton(text=city['city_name'], callback_data=city["destination_id"]))

    return destinations


def photo_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    item_yes = KeyboardButton(text='да')
    item_no = KeyboardButton(text='нет')
    markup.add(item_yes, item_no)
    return markup


#x = city_markup('париж')
#print(x)