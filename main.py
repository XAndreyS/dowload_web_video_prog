import requests
import json
import datetime
import time
from dowload_web_video_prog.load.download_video import downloads_serial_soup, downloads_film, downloads_content
from dowload_web_video_prog.load.download_video_async import executor_download_film, executor_download_serial_soup
from dowload_web_video_prog.data.get_link_sel import Serial
from dowload_web_video_prog.data.user_terminal_soup import run_user_terminal_soup
from dowload_web_video_prog.data.user_terminal_sel import run_user_terminal_selenium

with open('set_parser.json', encoding='utf8') as file:
    par_str = file.read()
    parser = json.loads(par_str)


def start(parser_set_user: dict):
    t_new = datetime.datetime.now()
    parser_set = parser_set_user
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
        if parser_set[str(1)] == 'bs4':
            run = run_user_terminal_soup()
        else:
            run = run_user_terminal_selenium()
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

    print('1:Для начала работы введите /start\n2:Для изменения настройки программы /settings\nЗакрыть программу /quit')


def settings():
    print('Доступно для настройки:\n1:Способ парсинга:\n    -bs4(по умолчанию)\n    -Selenium('
          'потребуется веб драйвер\n    '
          'Скачать https://chromedriver.chromium.org/downloads\n    '
          'Устаносить в папку data)\n2:Кол-во синхонной загрузки частей файла(для executor, по умолчнию 100)')
    print('Для изменения на сессию введите /lsettings\n'
          'Для глобального изменения введите /gsettins (не рекомендуется)')
    while True:
        try:
            user_input_set = str(input('Введите команду: '))
        except ValueError as error:
            print(error)
        else:
            if user_input_set == '/start':
                start(parser)
            elif user_input_set == '/help':
                help()
            elif user_input_set == '/quit':
                quit()
            elif user_input_set == '/lsettings' or user_input_set == '/ls':
                lsettings()
            elif user_input_set == 'gsettins' or user_input_set == '/qs':
                gsettings()


def lsettings():

    print(f'{1}: Выбрать парсер\n'
          f'{2}: Кол-во синхронных потоков при скачивания файла(chunk)\n'
          f'{3}: Изменить url сайта\n'
          f'{4}: Главное меню')
    while True:
        try:
            user_input_lset = int(input('Введите номер действия: '))
            if user_input_lset <= 0 or user_input_lset > 4:
                raise ValueError("Введите число соответствующее действия !!!")
        except ValueError as error:
            print(error)
        else:
            if user_input_lset == 4:
                help()
            elif user_input_lset == 1:
                lsettings_parser()
            elif user_input_lset == 2:
                lsettings_chunks()
            elif user_input_lset == 3:
                lsettings_url()


def lsettings_parser():
    ls_parser = {1: 'bs4', 2: 'selenium'}
    print(f'{1}: bs4\n{2}: Selenium')
    while True:
        try:
            user_input_lset = int(input('Введите номер парсера: '))
            if user_input_lset <= 0 or user_input_lset > 4:
                raise ValueError("Введите число соответствующее парсеру !!!")
        except ValueError as error:
            print(error)
        else:
            parser[str(1)] = ls_parser[user_input_lset]
            start(parser)
            main()


def lsettings_chunks():
    pass


def lsettings_url():
    pass


def gsettings():
    print(f'{1}: Парсер bs4\n'
          f'{2}: Парсер Selenium\n'
          f'{3}: Кол-во синхронных потоков при скачивании файла(chunk)\n'
          f'{4}: Изменить url сайта')


def main():

    print('Помощь /help\nЗакрыть программу /quit')
    while True:
        try:
            user_input_start = str(input('Для начала работы введите /start: '))
        except ValueError as error:
            print(error)
        else:
            if user_input_start == '/start':
                start(parser)
            elif user_input_start == '/help':
                help()
            elif user_input_start == '/settings' or user_input_start == '/ss':
                settings()
            elif user_input_start == '/quit':
                quit()


if __name__ == '__main__':

    main()

