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


QUERY_SEARCH = {
    'query': 'new_york',
    'locale': 'en_US',
    'currency': 'USD'
}
QUERY_PROPERTY_LIST = {
    'destinationId': '1506246',
    'pageNumber': '1',
    'pageSize': '25',
    'checkIn': '2020-01-08',
    'checkOut': '2020-01-15',
    'adults1': '1',
    'sortOrder': 'PRICE',
    'locale': 'en_US',
    'currency': 'USD'
}

QUERY_HOTELS = {
    'id': 242213,
    'name': 'Super 8 by Wyndham Paris IL',
    'address': '11642 Illinois Hwy 1',
    'price' : '$64',
    'City center distance': '2.1 miles'

}

QUERY_PHOTO = {'id': '1178275040'}


def get_website_request_city(message: str):
    """Функция обрабатывающая запрос пользователя для входа на сайт и поиск в нужном городе. """
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


def get_website_request_hotels(response):
    """Функция обрабатывающая запрос пользователя поиск  отелей в нужном городе. """
    # нужно достать id локации из response
    print("answ", response)
    QUERY_PROPERTY_LIST["destinationId"] = response
    response_hotels = requests.request("GET", URL_PROPERTY_LIST, headers=HEADERS, params=QUERY_PROPERTY_LIST, timeout=10)
    data = json.loads(response_hotels.text)

    hotels_list = list()
    for hotels in data["data"]["body"]["searchResults"]['results']:

        hotels_list.append({'photo_id': hotels['id'],
                            'name_hotel': hotels['name'],
                            'address_hotel': hotels['address']['streetAddress'],
                            'center_distance': hotels['landmarks'][0]['distance'],
                            'price': hotels['ratePlan']['price']['current']})

    return hotels_list


x = get_website_request_city('рим')
print(x[0]['destination_id'])
