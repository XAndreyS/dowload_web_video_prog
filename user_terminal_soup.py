import requests
from bs4 import BeautifulSoup
import time
from collections import defaultdict
import json
from get_link_soup import ZagonkaSoup
from download_video import downloads_serial_soup, downloads_film
from download_video_async import executor_download_serial_soup,executor_download_film


def first_user_search():
    url_zagonka = 'http://zagonko22.zagonko.com/'
    url_search = 'http://zagonko22.zagonko.com/engine/ajax/xsearch/f.php'
    while True:
        try:
            user_search = str(input('Введите название фильма/сериала: '))
            data_serch_list = ZagonkaSoup.searh_zagoka(url=url_search, search=user_search)
            if len(data_serch_list) == 0:
                raise ValueError("По вашему запросу ничего не найдено, повторите запрос")
        except ValueError as error:
            print(error)
        else:
            break
    count = 1
    for content in data_serch_list:
        print(f"{count}: {content['text']}")
        count += 1
    while True:
        try:
            user_num_content = int(input('Введите номер фильма/сериала: '))
            if user_num_content <= 0 or user_num_content > len(data_serch_list):
                raise ValueError("Введите число соответствующее номеру фильма/сериала!!!")
        except ValueError as error:
            print(error)
        else:
            break
    url_content = ZagonkaSoup.get_url_content(data_serch_list[int(user_num_content) - 1])
    name_content = ZagonkaSoup.get_name_content(data_serch_list[int(user_num_content) - 1])
    res_html = ZagonkaSoup.get_link_content(url_zagonka, url_content)
    id_content = ZagonkaSoup.get_id(data_serch_list[int(user_num_content) - 1])
    kpid_content = ZagonkaSoup.get_kpid(res_html)
    down_html = ZagonkaSoup.get_down_html(id_content, kpid_content)
    if 'сезон' in name_content.lower():
        link_serial = ZagonkaSoup.get_link_serial(down_html)
        return link_serial, name_content
    else:
        link_film = ZagonkaSoup.get_link_film(down_html, name_content)
        return link_film, name_content


def data_print_serial(data_serial: tuple, name_serial: str):
    count_series = []
    link_serial_dict = data_serial[0]
    translater_dict = data_serial[1]
    print(f"Выбран сериал {name_serial}")
    print('Количество сезонов:')
    count_sesons = 1

    for key in link_serial_dict:
        print(f'{count_sesons} Сезон: {translater_dict[key]}')
        count_sesons += 1

    while True:
        try:
            input_seson = int(input('Введите номер сезона: '))
            if input_seson <= 0 or input_seson > count_sesons:
                raise ValueError("Введите число соответствующее номеру сезона!!!")
        except ValueError as error:
            print(error)
        else:
            break

    print(f'Выбран {input_seson} Сезон, доступные переводы:')

    count_tanslater = translater_dict[str(input_seson)].replace("(", "").split(")")
    for i in range(len(count_tanslater)):
        if len(count_tanslater[i]) < 3:
            count_tanslater.pop(i)
        else:
            print(f'{i + 1}:{count_tanslater[i]}')

    while True:
        try:
            input_translater = int(input('Введите номер перевода/озвучки: '))
            if input_translater <= 0 or input_translater > len(count_tanslater):
                raise ValueError("Введите число соответствующее номеру перевода/озвучки!!!")
        except ValueError as error:
            print(error)
        else:
            break

    print('Выберете разрешение(качество) видео\n1: 240p\n2: 360p\n3: 480p')

    while True:
        try:
            input_video_resolution = int(input('Введите номер разрешения: '))
            if input_video_resolution <= 0 or input_video_resolution > 3:
                raise ValueError("Введите число соответствующее номеру разрешения!!!")
        except ValueError as error:
            print(error)
        else:
            break

    print(f'Скачать с серии')

    while True:
        try:
            input_count_series_in = int(input('Ведите номер серии для скачивания: '))
            if input_count_series_in <= 0 or input_count_series_in > 100:
                raise ValueError("Введите число соответствующее номеру серии!!!")
        except ValueError as error:
            print(error)
        else:
            break

    print(f'Скачать по серию включительно')

    while True:
        try:
            input_count_series_out = int(input('Ведите номер серии для скачивания: '))
            if input_count_series_out <= 0 or input_count_series_out > 100 \
                    or input_count_series_out < input_count_series_in:
                raise ValueError("Введите число соответствующее номеру серии,!!!")
        except ValueError as error:
            print(error)
        else:
            break

    print(f'скачать серии с {input_count_series_in} по {input_count_series_out}')
    count_series.append(input_count_series_in)
    count_series.append(input_count_series_out)

    return link_serial_dict[str(input_seson)][input_translater], input_video_resolution, count_series


def data_print_film(data_film: tuple, name_film: str):

    link_film_dict = data_film[0]
    translater_dict = data_film[1]
    name_film = name_film.split('(')[0].strip()
    print(f'Выбран фильм: {name_film}')
    print('Доступные переводы:')

    count = 1#
    for key in translater_dict:
        print(f'{key}: {translater_dict[key]}')
        count += 1

    while True:
        try:
            input_translater = int(input('Введите номер перевода/озвучки: '))
            if input_translater <= 0 or input_translater > count:
                raise ValueError("Введите число соответствующее номеру перевода/озвучки!!!")
        except ValueError as error:
            print(error)
        else:
            break

    print('Выберете разрешение(качество) видео\n1: 240p\n2: 360p\n3: 480p')

    while True:
        try:
            input_video_resolution = int(input('Введите номер разрешения: '))
            if input_video_resolution <= 0 or input_video_resolution > 3:
                raise ValueError("Введите число соответствующее номеру разрешения!!!")
        except ValueError as error:
            print(error)
        else:
            break

    return link_film_dict[name_film][input_translater], input_video_resolution, name_film


def run_user_terminal():
    first_data_user = first_user_search()

    if 'сезон' in first_data_user[1]:
        data_serial = data_print_serial(first_data_user[0], first_data_user[1])
    else:
        data_film = data_print_film(first_data_user[0], first_data_user[1])

    print('Выберете способ скачивния:')
    print('1) Обычный')
    print('2) Ассинхнонный - На данный момеент этот  сособ экспереементальный\nи может привеести к ошибкам')
    while True:
        try:
            user_input_download = int(input('Введите номер способа загрузки видео: '))
            if user_input_download < 0 or user_input_download > 3:
                raise ValueError("Введите число соответствующее номеру сервиса!!!")
        except ValueError as error:
            print(error)
        else:
            break
    if user_input_download == 1:
        if 'сезон' in first_data_user[1]:
            downloads_serial_soup(data_serial[0], data_serial[1], data_serial[2])
        else:
            downloads_film(data_film[0], data_film[1], data_film[2])
    else:
        if 'сезон' in first_data_user[1]:
            executor_download_serial_soup(data_serial[0], data_serial[1], data_serial[2])
        else:
            executor_download_film(data_film[0], data_film[1], data_film[2])


def main():
    pass

#СамоИрония судьбы
#Виват, гардемарины!
#Иван Васильевич меняет профессию
#цельнометалл
if __name__ == '__main__':

    main()


# https://www.tiktok.com/@genarochambi600/video/7229480740478586117?is_from_webapp=1&sender_device=pc