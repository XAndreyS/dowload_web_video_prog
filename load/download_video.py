import requests
import json
import datetime


def downloads_serial_sel(url_list, video_resolution, count_series):
    """Последовательное скачивание файлов(сериалы)"""
    count_in = 1
    count_out = count_series[1]
    print(f'Скачивание началось!!!!!!!\nВсего для скачивания {count_out} видео\n============')
    try:
        for count_url in range(count_series[0], count_series[1]+1):
            t_new = datetime.datetime.now()
            print(f'Скачивается {count_in} видео файл')
            response = requests.get(url=url_list[0][video_resolution-1][count_url-1], stream=True)
            with open(f'files/{count_url}_seria.mp4', 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        file.write(chunk)
            print(f'Время скачивания файла:{datetime.datetime.now() - t_new}')
            print(f'Осталось скачать {count_out-1} видео файл/файлов')
            count_in += 1
            count_out -= 1
        return 'Video download'
    except Exception as ex:
        return 'Upps Eror'


def downloads_serial_soup(url_list, video_resolution, count_series):
    """Последовательное скачивание файлов(сериалы)"""
    url_list_all = url_list
    response_list = []
    https = 'https:'
    count_series = count_series
    count_in = 1
    count_out = count_series[1]
    print(f'Скачивание началось!!!!!!!\nВсего для скачивания {count_out} видео\n============')
    try:
        for count_url in range(count_series[0], count_series[1]+1):
            t_new = datetime.datetime.now()
            print(f'Скачивается {count_in} видео файл')
            response = requests.get(url=https+url_list[0][video_resolution-1][count_url-1], stream=True)
            with open(f'files/{count_url}_seria.mp4', 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        file.write(chunk)
            print(f'Время скачивания файла:{datetime.datetime.now() - t_new}')
            print(f'Осталось скачать {count_out-1} видео файл/файлов')
            count_in += 1
            count_out -= 1
        return 'Video download'
    except Exception as ex:
        return 'Upps Eror'


def downloads_film(url_list, video_resolution, film_name):
    """Последовательное скачивание файлов(фильмы)"""
    url_list = url_list
    video_resolution = video_resolution
    film_name = film_name.split("(")[0]
    count = 0
    print(f'Скачивание началось!!!!!!!\n============')
    try:
        t_new = datetime.datetime.now()
        print(f'Скачивается видео файл\nПримерное время скачивания файла в разрешении 480p: 4 минуты')
        response = requests.get(url=url_list[video_resolution-1],stream=True)
        with open(f'files/{film_name}.mp4', 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    file.write(chunk)
        print(f'Время скачивания файла:{datetime.datetime.now() - t_new}')

        return 'Video download'
    except Exception as ex:
        return 'Upps Eror'


def downloads_film_soup(url_list, video_resolution, film_name):
    """Последовательное скачивание файлов(фильмы)"""
    url_list = url_list
    https = 'https:'
    video_resolution = video_resolution
    film_name = film_name.split("(")[0]
    count = 0
    print(f'Скачивание началось!!!!!!!\n============')
    try:
        t_new = datetime.datetime.now()
        print(f'Скачивается видео файл\nПримерное время скачивания файла в разрешении 480p: 4 минуты')
        response = requests.get(url=https+url_list[video_resolution-1],stream=True)
        with open(f'files/{film_name}.mp4', 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    file.write(chunk)
        print(f'Время скачивания файла:{datetime.datetime.now() - t_new}')

        return 'Video download'
    except Exception as ex:
        return 'Upps Eror'


def downloads_content(url:str):
    """Последовательное скачивание файлов(фильмы)"""
    url = url

    count = 0
    print(f'Скачивание началось!!!!!!!\n============')
    try:
        t_new = datetime.datetime.now()
        print(f'Скачивается видео файл\nПримерное время скачивания файла в разрешении 480p: 4 минуты')
        response = requests.get(url=url,stream=True)
        with open(f'files/Video.mp4', 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    print(count)
                    count+=1
                    file.write(chunk)
        print(f'Время скачивания файла:{datetime.datetime.now() - t_new}')

        return 'Video download'
    except Exception as ex:
        return 'Upps Eror'



def main():
    pass


if __name__ == '__main__':
    main()
