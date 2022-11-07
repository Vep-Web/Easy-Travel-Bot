from loader import bot
from states.contact_info import User
from telebot.types import Message, InputMediaPhoto
from config_data.config_site import get_website_request_hotels, sorted_list_hotels, get_website_request_photo
from keyboards.reply.city import city_markup, count_markup, photo_markup
from keyboards.reply.calendars import set_arrival_date
from handlers.custom_heandltrs import history
from datetime import datetime


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal', 'history'])
def start(message: Message) -> None:
    """
    Функция, запускающая команду: 'lowprice'. Начинает сбор информации по запросу и запрашивает город
    для поиска отелей.

    :param message: Message
    :return: None
    """
    user = User.get_user(message.from_user.id)

    if message.text == '/lowprice':
        user.command = message.text
        user.request_time = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        bot.send_message(message.from_user.id, f'Отлично, Вы выбрали поиск отелей по низкой цене.')
        return set_arrival_date(message)

    elif message.text == '/highprice':
        user.flag = True
        user.command = message.text
        user.request_time = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        bot.send_message(message.from_user.id, f'Отлично, Вы выбрали поиск отелей по высокой цене.')
        return set_arrival_date(message)

    elif message.text == '/bestdeal':
        user.command = message.text
        user.request_time = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        bot.send_message(message.from_user.id, f'Отлично, Вы выбрали поиск лучших вариантов.')
        return set_arrival_date(message)

    elif message.text == "/history":
        history.show_history(message)


#Проверка на ввод с клавиатуры
def city(message) -> None:
    user = User.get_user(message.from_user.id)

    if message:
        if user.command == '/lowprice' or user.command == '/highprice':
            chat = bot.send_message(message.from_user.id, "Введите название города и я приступлю к поиску.")
            bot.register_next_step_handler(chat, get_cities)
        else:
            chat = bot.send_message(message.from_user.id, f'Введите минимальную стоимость отеля долларах.')
            bot.register_next_step_handler(chat, get_min_price)


def get_min_price(message: Message) -> None:
    user = User.get_user(message.from_user.id)
    if message.text.isdigit():
        user.min_price = message.text
        chat = bot.send_message(message.chat.id, f'Введите максимальную стоимость отеля в долларах.')
        bot.register_next_step_handler(chat, get_max_price)
    else:
        chat = bot.send_message(message.chat.id, f'Стоимость не может быть буквой.') # авто переход на пред-щую функцию city
        bot.register_next_step_handler(chat, city)


#@bot.message_handler(content_types='text')
def get_max_price(message: Message) -> None:
    user = User.get_user(message.from_user.id)
    if message.text.isdigit():
        user.max_price = message.text
        chat = bot.send_message(message.from_user.id, f'Отлично, а теперь введите желаемое растояние до центра города в '
                                                 f'километрах.')
        bot.register_next_step_handler(chat, get_range)
    else:
        bot.send_message(message.chat.id, f'Стоимость не может быть буквой.') # авто переход на пред-щую функцию city


#@bot.message_handler(content_types='text')
def get_range(message: Message) -> None:
    user = User.get_user(message.from_user.id)
    if message.text.isdigit():
        user.range = message.text
        chat = bot.send_message(message.chat.id, f'Введите название города и я приступлю к поиску.')
        bot.register_next_step_handler(chat, get_cities)
    else:
        bot.send_message(message.chat.id, f'Расстояние не может быть буквой.')


#@bot.message_handler(content_types='text')
def get_cities(message: Message) -> None:
    """
    Функция, проверяет входящий тип данных из предыдущей функции и уточняет более точный адрес.

    :param message: Message
    :return: None
    """
    user = User.get_user(message.from_user.id)
    if message.text.isalpha():
        user.city = message.text
        markup = city_markup(message.text)
        bot.send_message(message.from_user.id, 'Уточните пожалуйста страну и район поиска:', reply_markup=markup)

    else:
        bot.send_message(message.from_user.id, f'Имя не может начинаться с числа.')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline_city(call):
    """
    Функция- обработчик inline-кнопок. Реагирует только на информацию из кнопок
    выбора города и запрашивает у пользователя колличество отелей для поиска.

    :param call: Message
    :return: None
    """
    user = User.get_user(call.message.chat.id)

    if call.data.isdigit():
        get_website_request_hotels(call.data, user.user_id)
        markup_num = count_markup()
        chat = bot.send_message(call.message.chat.id, f'Сколько отелей показать?', reply_markup=markup_num)
        bot.register_next_step_handler(chat, get_photo)

    else:
        bot.send_message(call.message.from_user.id, f'Имя не может начинаться с числа.')


#@bot.message_handler(content_types='text')
def get_photo(message: Message) -> None:
    """
    Функция- обработчик reply-кнопок. Реагирует только на информацию из кнопок
    и запрашивает показ фотографий.


    :param message: Message
    :return: None
    """
    if message.text.isdigit():
        user = User.get_user(message.from_user.id)
        user.hotels_number_to_show = message.text
        markup = photo_markup()
        chat = bot.send_message(message.chat.id, f'Показывать фото отелей?', reply_markup=markup)
        bot.register_next_step_handler(chat, get_photo_count)

    else:
        bot.send_message(message.from_user.id, f'Нужно нажать на кнопу.')


#@bot.message_handler(content_types='text')
def get_photo_count(message: Message) -> None:
    """
    Функция- обработчик reply-кнопок. Реагирует только на информацию из кнопок
    и обрабатывает запрос от кнопок, для продолжения по сценарию.

    :param message: Message
    :return: None
    """
    user = User.get_user(message.from_user.id)

    if message.text == 'да':
        markup = count_markup()
        chat = bot.send_message(message.from_user.id, f'Сколько фото показать?', reply_markup=markup)
        bot.register_next_step_handler(chat, final)

    elif message.text == 'нет':
        bot.send_message(message.chat.id, f'Хорошо. Держи список отелей.')
        list_hotels = sorted_list_hotels(user.hotels_number_to_show, user.flag)
        text_for_database = ""

        for hotel in list_hotels:
            text = f"Название отеля: {hotel['name_hotel']} \nАдрес: {hotel['address_hotel']}" \
                   f" \nДо центра: {hotel['center_distance']} \nЦена за сутки: {hotel['price']}" \
                   f" \nЦена за период проживания c {user.arrival_date} по {user.departure_date}: " \
                   f"{hotel['price_for_period']} \nСайт отеля: {hotel['website']}"
            bot.send_message(message.from_user.id, "".join(text))

            text_for_database += f"{hotel['name_hotel']};"

        history.add_user_data(user.user_id, user.command, user.request_time, text_for_database)

    else:
        bot.send_message(message.from_user.id, f'Нужно нажать на кнопу.')


#@bot.message_handler(content_types='text')
def final(message: Message) -> None:
    """
    Функция- обработчик reply-кнопок. Реагирует только на информацию из кнопок
    и обрабатывает запрос от кнопок. Финальная функция завершающая сценарий, выводит пользователю результаты
    его запросов.

    :param message: Message
    :return: None
    """
    user = User.get_user(message.from_user.id)
    user.photos_num = message.text

    if message.text.isdigit():
        bot.send_message(message.from_user.id, f"Начинаю поиск...")

        count_photo = message.text
        list_hotels = sorted_list_hotels(user.hotels_number_to_show, user.flag)
        list_photo = get_website_request_photo(list_hotels, count_photo)
        text_for_database = ""
        media_group = list()
        index = 0

        for hotel in list_hotels:
            text = f"Название отеля: {hotel['name_hotel']} \nАдрес: {hotel['address_hotel']}" \
                   f" \nДо центра: {hotel['center_distance']} \nЦена за сутки: {hotel['price']}" \
                   f" \nЦена за период проживания c {user.arrival_date} по {user.departure_date}: " \
                   f"{hotel['price_for_period']} \nСайт отеля: {hotel['website']}"

            text_for_database += f"{hotel['name_hotel']};"

            for i in range(int(count_photo)):
                media_group.append(InputMediaPhoto(media=list_photo[index], caption=text if i == 0 else ''))
                index += 1

            bot.send_media_group(message.chat.id, media=media_group)
            media_group.clear()

        history.add_user_data(user.user_id, user.command, user.request_time, text_for_database)

    else:
        bot.send_message(message.from_user.id, f'Нужно нажать на кнопу.')

