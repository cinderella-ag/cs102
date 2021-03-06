import requests
import time
import random

import config


def get(url, params=({}), timeout=5, max_retries=5, backoff_factor=1.3):
    """ Выполнить GET-запрос
    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    retries = 0
    delay = 0.1
    while retries < max_retries:
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            time.sleep(delay)
            delay = delay * backoff_factor + random.uniform(0, 0.1)
            retries += 1
        else:
            if 'error' in response.json():
                time.sleep(delay)
                delay = delay * backoff_factor + random.uniform(0, 0.1)
                retries += 1
            else:
                return response
    return False


def get_friends(user_id, fields):
    """ Вернуть данных о друзьях пользователя
    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    domain = config.VK_CONFIG['domain']
    access_token = config.VK_CONFIG['access_token']
    v = config.VK_CONFIG['version']

    query = f"{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={v}"
    response = get(url=query)
    try:
        return response.json()['response']['items']
    except:
        return None


if __name__ == "__main__":
    friends = get_friends(759373, 'first_name')

    with open('jean_friends.txt', 'w', encoding='utf-8') as file:
        n = 0
        for fr in friends:
            string = str(n) + ' ' + fr['first_name'] + ' ' + fr['last_name'] + '\n'
            file.write(string)
            n += 1
