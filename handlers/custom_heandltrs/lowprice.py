from loader import bot
from states.contact_info import UserState
from telebot.types import Message
from config_data.config_site import get_website_request_hotels, sorted_list_hotels, get_website_request_photo
from keyboards.reply.city import city_markup, count_markup, photo_markup


@bot.message_handler(commands=['lowprice'])
def start(message: Message) -> None:
    """
    Функция, запускающая команду: 'lowprice'. Начинает сбор информации по запросу и запрашивает город
    для поиска отелей.

    :param message: Message
    :return: None
    """
    bot.send_message(message.from_user.id, f'Отлично Вы выбрали поиск отелей по низкой цене.')
    bot.set_state(message.from_user.id, UserState.cities, message.chat.id)
    bot.send_message(message.from_user.id, f'Введите название города и я приступлю к поиску.')


@bot.message_handler(state=UserState.cities)
def get_cities(message: Message) -> None:
    """
    Функция, проверяет входящий тип данных из предыдущей функции и уточняет более точный адрес.

    :param message: Message
    :return: None
    """
    if message.text.isalpha():
        markup = city_markup(message.text)
        bot.send_message(message.from_user.id, 'Уточните пожалуйста:', reply_markup=markup)

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

    if call.data.isdigit():
        get_website_request_hotels(call.data)
        markup_num = count_markup()
        chat = bot.send_message(call.message.chat.id, f'Сколько отелей показать?', reply_markup=markup_num)
        bot.register_next_step_handler(chat, get_photo)


@bot.message_handler(state=UserState.count_hotels)
def get_photo(message: Message) -> None:
    """
    Функция- обработчик reply-кнопок. Реагирует только на информацию из кнопок
    и запрашивает показ фотографий.


    :param message: Message
    :return: None
    """
    if message.text.isdigit():
        markup = photo_markup()
        bot.set_state(message.from_user.id, UserState.photo, message.chat.id)
        chat = bot.send_message(message.chat.id, f'Показывать фото отелей?', reply_markup=markup)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['count_cities'] = message.text
        bot.register_next_step_handler(chat, get_photo_count)

    else:
        bot.send_message(message.from_user.id, f'Нужно нажать на кнопу.')


@bot.message_handler(state=UserState.photo)
def get_photo_count(message: Message) -> None:
    """
    Функция- обработчик reply-кнопок. Реагирует только на информацию из кнопок
    и обрабатывает запрос от кнопок, для продолжения по сценарию.

    :param message: Message
    :return: None
    """
    if message.text == 'да':
        markup = count_markup()
        bot.set_state(message.from_user.id, UserState.count_photo, message.chat.id)
        bot.send_message(message.from_user.id, f'Сколько фото показать?', reply_markup=markup)

    elif message.text == 'нет':
        bot.send_message(message.chat.id, f'Хорошо. Держи список отелей.')

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            count_cities = data['count_cities']
            list_hotels = sorted_list_hotels(count_cities)

            for hotel in list_hotels:
                text = f"Название отеля: {hotel['name_hotel']} \nАдрес: {hotel['address_hotel']}" \
                       f" \nДо центра: {hotel['center_distance']} \nЦена за сутки: {hotel['price']}"
                bot.send_message(message.from_user.id, "".join(text))

    else:
        bot.send_message(message.from_user.id, f'Нужно нажать на кнопу.')


@bot.message_handler(state=UserState.count_photo)
def final(message: Message) -> None:
    """
    Функция- обработчик reply-кнопок. Реагирует только на информацию из кнопок
    и обрабатывает запрос от кнопок. Финальная функция завершающая сценарий, выводит пользователю результаты
    его запросов.

    :param message: Message
    :return: None
    """
    if message.text.isdigit():
        bot.set_state(message.from_user.id, UserState.count_photo, message.chat.id)
        bot.send_message(message.from_user.id, f"Начинаю поиск...")

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            count_photo = message.text
            count_cities = data['count_cities']
            list_hotels = sorted_list_hotels(count_cities)
            list_photo = get_website_request_photo(list_hotels, count_photo)
            index = 0

            for hotel in list_hotels:
                text = f"Название отеля: {hotel['name_hotel']} \nАдрес: {hotel['address_hotel']}" \
                       f" \nДо центра: {hotel['center_distance']} \nЦена за сутки: {hotel['price']}"

                bot.send_message(message.from_user.id, "".join(text))
                move = 0
                while move != int(count_photo):
                    photo = list_photo[index]
                    bot.send_photo(message.chat.id, photo=photo)
                    move += 1
                    index += 1

    else:
        bot.send_message(message.from_user.id, f'Нужно нажать на кнопу.')
