import requests
import json
import datetime
import time
from download_video import downloads_serial, downloads_film
from download_video_async import executor_download_serial
from get_link_sel import Serial


def data_print_serial(data_link: dict, data_translater: dict):
    """На вход принимает результат работы функции Serial.get_link(словарь data_link:{int(номер сезона){int(номер сезона)
    или str(с именем перевода)=[([ссылки на  видео])]}},
    словарь data_translater: содержит имена переводовпо сезонам, т.к. возникла проблема с локаторами
     в словаре data_link сожержится int если переводов более одного.
      На выход
      1)своеобразный списоксо ссылками  на видео после выбора пользователя,
      2)номер качества видеео для его выбора из списка пункта 1,
      3)Список серий для скачивания)"""
    sesons_list = []
    traslater_list_one = []
    count_series = []
    serial_link = data_link
    serial_tanslater = data_translater
    print(f'Количество сезонов:')
    for key_1 in serial_link:
        if len(serial_tanslater[int(key_1[0])]) > 3:
            print(f'{key_1}:{serial_tanslater[int(key_1[0])]}')
    for key_1 in serial_link:
        sesons_list.append(key_1)
        for key_2 in serial_link[key_1]:
            if type(key_2) is int:
                if len(serial_tanslater[key_1[0]]) > 3:
                    print(f'Переводы:{key_1} :{key_2}:{serial_tanslater[key_1[0]]}')
            else:
                traslater_list_one.append(key_2)
    while True:
        try:
            input_sezon = int(input('Введите номер Сезона'))
        except ValueError as error:
            print("Не верный ввод!!!!!\nВедите тоько цифры соответствующие номеру сезона")
        else:
            break
    print(f'Выбран {input_sezon}, доступные переводы:')
    count_tanslater = serial_tanslater[input_sezon].replace("(", "").split(")")
    for i in range(len(count_tanslater)):
        if len(count_tanslater[i]) < 3:
            count_tanslater.pop(i)
        else:
            print(f'{i+1}:{count_tanslater[i]}')
    while True:
        try:
            input_tanslater = int(input('Введите номер перевода'))
        except ValueError as error:
            print("Не верный ввод!!!!!\nВедите тоько цифры соответствующие номеру сезона")
        else:
            break
    print('Выберете разрешение(качество) видео\n1: 240p\n2: 360p\n3: 480p')
    while True:
        try:
            input_video_resolution = int(input('Введите номер разрешения'))
        except ValueError as error:
            print("Не верный ввод!!!!!\nВедите тоько цифры соответствующие номеру разрешения")
        else:
            break
    print(f'Скачать с серии')
    while True:
        try:
            input_count_series_in = int(input('Ведите номер серии для скачивания'))
        except ValueError as error:
            print("Не верный ввод!!!!!\nВедите тоько цифры соответствующие номеру серии")
        else:
            break
    print(f'Скачать по серию включительно')
    while True:
        try:
            input_count_series_out = int(input('Ведите номер серии для скачивания'))
        except ValueError as error:
            print(error)
            print("Не верный ввод!!!!!\nВедите тоько цифры соответствующие номеру серии")
        else:
            break
    print(f'скачать серии с {input_count_series_in} по {input_count_series_out}')
    count_series.append(input_count_series_in)
    count_series.append(input_count_series_out)
    if len(count_tanslater) > 1:
        return serial_link[f'{input_sezon} Сезон'][input_tanslater], input_video_resolution, count_series
    else:
        return serial_link[f'{input_sezon} Сезон'][serial_tanslater[input_sezon]], input_video_resolution, count_series


def data_print_film(data_link: dict, data_translater: dict):
    """Сбор данных от пользователя в консоли, для последующей отправки в  функцию скачивания(фильмы)
    подробнее пока в функции data_print_serial()"""
    film_link = data_link
    film_tanslater = data_translater
    print('Доступные переводы:')
    count = 1
    film_name = ''
    for key_1 in film_tanslater:
        print(f'{key_1}: {film_tanslater[key_1]}')
        count += 1

    # Получим название фильма из ключа, что бы передать его в функцию скачивания, для имени файла
    for key_1 in film_link:
        film_name = key_1
    while True:
        try:
            input_translater = int(input('Введите номер перевода'))
        except ValueError as error:
            print("Не верный ввод!!!!!\nВедите тоько цифры соответствующие номеру перевода")
        else:
            break
    print('Выберете разрешение(качество) видео\n1: 240p\n2: 360p\n3: 480p')
    while True:
        try:
            input_video_resolution = int(input('Введите номер разрешения'))
        except ValueError as error:
            print("Не верный ввод!!!!!\nВедите тоько цифры соответствующие номеру разрешения")
        else:
            break

    return film_link[film_name][input_translater], input_video_resolution, film_name


def main():

    get_link = Serial('http://zagonka1.zagonkov.gb.net/').get_link()
    print(get_link.url)
    if get_link[2] == 'сериал':
        print_sort = data_print_serial(get_link[0], get_link[1])
        #download_serials = downloads_serial(print_sort[0], print_sort[1], print_sort[2])
        download_serials = executor_download_serial(print_sort[0], print_sort[1], print_sort[2])

    elif get_link[2] == 'фильм':
        print_sort = data_print_film(get_link[0], get_link[1])
        print(len(print_sort[0]))
        print(print_sort[2])
        download_films = downloads_film(print_sort[0], print_sort[1], print_sort[2])


if __name__ == '__main__':

    main()