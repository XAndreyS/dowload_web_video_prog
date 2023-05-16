import requests
import json
import datetime
import time
from dowload_web_video_prog.load.download_video import downloads_serial_soup, downloads_film, downloads_content
from dowload_web_video_prog.load.download_video_async import executor_download_film, executor_download_serial_soup
from dowload_web_video_prog.data.get_link_sel import Serial
from dowload_web_video_prog.data.user_terminal_soup import run_user_terminal_soup


def start():
    t_new = datetime.datetime.now()
    print('Достуные сайты для скачивания видео:')
    print('1: Загонка\n2: другое')
    while True:
        try:
            user_input_service = int(input('Введите номер сайта: '))
            if user_input_service < 0 or user_input_service > 3:
                raise ValueError("Введите число соответствующее номеру сервиса!!!")
        except ValueError as error:
            print(error)
        else:
            break
    if user_input_service == 1:
        run = run_user_terminal_soup()
    else:
        while True:
            try:
                user_input_url = str(input('Введите cссылку на видео: '))
            except ValueError as error:
                print(error)
            else:
                break
        downloads_content(user_input_url)
    print(f'Время скачивания файлов:{datetime.datetime.now() - t_new}')


def help():

    print('1:Для начала работы введите /start\n2:Для изменения настройки программы /settings')


def settings():
    print('Доступно для настройки:\n1:Способ парсинга:\n    -bs4(по умолчанию)\n    -Selenium('
          'потребуется веб драйвер\n    '
          'Скачать https://chromedriver.chromium.org/downloads\n    '
          'Устаносить в папку data)\n2:Кол-во синхонной загрузки частей файла(для executor, по умолчнию 100)')
    print('Для изменения на сессию введите /lseettings\n'
          'Для глобального изменения введите /gsettins (не рекомендуется)')
    while True:
        try:
            user_input_set = str(input('Введите команду: '))
        except ValueError as error:
            print(error)
        else:
            if user_input_set == '/start':
                start()
            elif user_input_set == '/help':
                help()
            elif user_input_set == '/lsettings':
                lsettings()
            elif user_input_set == 'gsettins':
                gsettings()


def lsettings():
    pass


def gsettings():
    pass


def main():
    print('Помощь /help')
    while True:
        try:
            user_input_start = str(input('Для начала работы введите /start: '))
        except ValueError as error:
            print(error)
        else:
            if user_input_start == '/start':
                start()
            elif user_input_start == '/help':
                help()
            elif user_input_start == '/settings':
                settings()





if __name__ == '__main__':

    main()


# https://www.tiktok.com/@babycoma13/video/6960334367952489729?is_from_webapp=1&sender_device=pc