from config_data.config import RAPID_API_KEY
import requests
import json
import re

HEADERS = {
    'X-RapidAPI-Host': 'hotels4.p.rapidapi.com',
    'X-RapidAPI-Key': RAPID_API_KEY
}


URL_SEARCH = 'https://hotels4.p.rapidapi.com/locations/v2/search'
URL_PROPERTY_LIST = 'https://hotels4.p.rapidapi.com/properties/list'
URL_PHOTO = 'https://hotels4.p.rapidapi.com/properties/get-hotel-photos'
URL_HOTEL = 'https://hotels4.p.rapidapi.com/properties/get-details'


QUERY_SEARCH = dict()
QUERY_PROPERTY_LIST = dict()
QUERY_HOTELS = dict()
QUERY_PHOTO = dict()
hotels_list = list()


def get_website_request_city(message: str) -> list:
    """
    Функция делает get-запрос для поиска города и возвращает для уточнения пользователю ближайшие места поиска.

    :param message: str
    :return: list
    """
    QUERY_SEARCH["query"] = message

    response = requests.get(URL_SEARCH, headers=HEADERS, params=QUERY_SEARCH, timeout=10)
    if response.status_code == requests.codes.ok:
        pattern = r'(?<="CITY_GROUP",).+?[\]]'
        find = re.search(pattern, response.text)
        if find:
            result = json.loads(f"{{{find[0]}}}")

            cities = list()
            for dest_id in result['entities']:
                cities.append({'city_name': dest_id['caption'], 'destination_id': dest_id['destinationId']})

            return cities


def get_website_request_hotels(response: str) -> list:
    """
    Функция делает get-запрос для поиска отелей в выбранном городе и возвращает список найденных отелей.

    :param response: str
    :return: list
    """

    QUERY_PROPERTY_LIST["destinationId"] = response
    response_hotel = requests.request("GET", URL_PROPERTY_LIST, headers=HEADERS, params=QUERY_PROPERTY_LIST, timeout=10)
    data = json.loads(response_hotel.text)

    for hotels in data["data"]["body"]["searchResults"]['results']:

        try:
            hotel_info = {'photo_id': hotels['id'],
                          'name_hotel': hotels['name'],
                          'address_hotel': hotels['address']['streetAddress'],
                          'center_distance': hotels['landmarks'][0]['distance'],
                          'price': hotels['ratePlan']['price']['current']
                          }

            hotels_list.append(hotel_info)

        except KeyError:
            pass

    return hotels_list


def sorted_list_hotels(count_cities: str) -> list:
    """
    Функция сортирующая список отелей по цене.

    :param count_cities: str
    :return: list
    """
    final_list_hotels = list()
    list_sorted = sorted(hotels_list, key=lambda x: int(x['price'].replace("$", '')), reverse=False)
    move = 0
    for hotels in list_sorted:
        if move != int(count_cities):
            final_list_hotels.append(hotels)
            move += 1

    return final_list_hotels


def get_website_request_photo(list_hotels: list, count: str) -> list:
    """
    Функция делает get-запрос для поиска фотографий отелей.

    :param list_hotels: list
    :param count: str
    :return: list
    """
    list_photo = list()

    for hotel_info in list_hotels:
        QUERY_PHOTO['id'] = hotel_info['photo_id']
        response = requests.request("GET", URL_PHOTO, headers=HEADERS, params=QUERY_PHOTO, timeout=10)
        data = json.loads(response.text)
        move = 0

        for info_images in data['hotelImages']:
            if move != int(count):
                images = info_images['baseUrl'].replace("{size}", "y")
                list_photo.append(images)
                move += 1

    return list_photo
