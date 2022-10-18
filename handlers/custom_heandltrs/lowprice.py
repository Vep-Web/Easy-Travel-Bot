from loader import bot
from states.contact_info import UserState
from telebot.types import Message
from config_data.config_site import get_website_request_hotels
from keyboards.reply.city import city_markup, photo_markup
from telebot import types


@bot.message_handler(commands=['lowprice'])
def start(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Отлично Вы выбрали поиск отелей по низкой цене.')
    bot.set_state(message.from_user.id, UserState.cities, message.chat.id)
    bot.send_message(message.from_user.id, f'Введите название города и я приступлю к поиску.')


@bot.message_handler(state=UserState.cities)
def get_cities(message: Message) -> None:
    if message.text.isalpha():
        markup = city_markup(message.text)
        bot.set_state(message.from_user.id, UserState.count_hotels, message.chat.id)
        bot.send_message(message.from_user.id, 'В каком городе ищем?', reply_markup=markup)
    else:
        bot.send_message(message.from_user.id, f'Имя не может начинаться с числа.')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

    if call.message:
        answer = get_website_request_hotels(call.message)

        with bot.retrieve_data(answer) as data:
            data['cities'] = answer

        bot.register_next_step_handler(get_photo)

    else:
        bot.send_message(call.message.from_user.id, f'Для точного поиска нужно выбрать из списка.')
        bot.register_next_step_handler(get_cities)


@bot.message_handler(state=UserState.cities)
def get_photo(message: Message) -> None:
    bot.set_state(message.from_user.id, UserState.photo, message.chat.id)
    bot.send_message(message.from_user.id, f'Показывать фото отелей?', reply_markup=photo_markup())



@bot.message_handler(state=UserState.photo)
def get_photo(message: Message) -> None:
    # кнопка на показ колва фото
    bot.set_state(message.from_user.id, UserState.count_photo, message.chat.id)
    bot.send_message(message.from_user.id, f'Сколько фото показать?')


@bot.message_handler(state=UserState.count_photo)
def get_count_photo(message: Message) -> None:

    bot.send_message()