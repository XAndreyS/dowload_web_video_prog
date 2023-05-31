
import json
import datetime
from load.download_video import downloads_serial_soup, downloads_film, downloads_content
from load.download_video_async import executor_download_film, executor_download_serial_soup
from data.get_link_sel import Serial
from data.user_terminal_soup import run_user_terminal_soup
from data.user_terminal_sel import run_user_terminal_selenium
from settings.settings import set_zagonka, set_executor_download

with open('settings/set_parser.json', encoding='utf8') as file:
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
    print('===Доступно для настройки===:\n1: Способ парсинга:\n    -bs4(по умолчанию)\n    -Selenium('
          'потребуется веб драйвер\n    '
          'Скачать https://chromedriver.chromium.org/downloads\n    '
          'Устаносить в папку data)\n2:Кол-во синхонной загрузки частей файла(для executor, по умолчнию 100)')
    print('2: Кол-во синхронных загрузок:\n     '
          '-Для скачивания фильма(по умолчанию 100)\n    '
          '-Для скачивания нескольких серий сериала(по умолчанию 20)\n')
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
            elif user_input_set == 'gsettins' or user_input_set == '/gs':
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
                lsettings_max_workers()
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


def lsettings_max_workers():
    print(f'1: Кол-во синхронных частей скачивания фильма(по умолчанию {set_executor_download["max_workers_file"]})\n'
          f'2: Кол-во синхронных скачиваний серий сериалов(по умолчанию {set_executor_download["max_workers_files"]})\n')
    while True:
        try:
            user_input_lset_mw = int(input('Введите номер действия: '))
            if user_input_lset_mw <= 0 or user_input_lset_mw > 3:
                raise ValueError("Введите число соответствующее действию !!!")
        except ValueError as error:
            print(error)
        else:
            if user_input_lset_mw == 1:
                while True:
                    try:
                        user_input_lset_mw_f = int(input('Введите кол-во chunks(макс-1000): '))
                        if user_input_lset_mw_f <= 0 or user_input_lset_mw_f > 1001:
                            raise ValueError("Введите число от 0 до 1000 !!!")
                    except ValueError as error:
                        print(error)
                    else:
                        set_executor_download['max_workers_file'] = user_input_lset_mw_f
            else:
                while True:
                    try:
                        user_input_lset_mw_s = int(input('Введите кол-во chunks(макс-100): '))
                        if user_input_lset_mw_s <= 0 or user_input_lset_mw_s > 100:
                            raise ValueError("Введите число от 0 до 100 !!!")
                    except ValueError as error:
                        print(error)
                    else:
                        set_executor_download['max_workers_files'] = user_input_lset_mw_s


def lsettings_url():
    print('Введите новый url сайта в формате: http://zagonka27.zagonko.com/ '
          '\nВнимание!!! При коппировании url из браузера url можетбыть таким http://zagonka27.zagonko.com/9,'
          ' вводите без 9')
    while True:
        try:
            user_input_lset_url = str(input('Введите новый url: '))

        except ValueError as error:
            print(error)
        else:
            old_set_zagonka = set_zagonka
            old_url = set_zagonka['zagonka_urls']['url']
            print(old_url)
            for key in set_zagonka:
                for key_2 in set_zagonka[key]:
                    print(set_zagonka[key][key_2])
                    if type(set_zagonka[key][key_2]) is str:
                        if 'http' in set_zagonka[key][key_2]:
                            set_zagonka[key][key_2]=old_set_zagonka[key][key_2].replace(f'{old_url}', f'{user_input_lset_url}')
            print('Изменения настроек на сессию:')
            print(set_zagonka)
            start(parser)
            main()


def gsettings():

    print(f'{1}: Выбрать парсер\n'
          f'{2}: Кол-во синхронных потоков при скачивания файла(chunk)\n'
          f'{3}: Изменить url сайта\n'
          f'{4}: Главное меню')
    while True:
        try:
            user_input_gset = int(input('Введите номер действия: '))
            if user_input_gset <= 0 or user_input_gset > 4:
                raise ValueError("Введите число соответствующее действия !!!")
        except ValueError as error:
            print(error)
        else:
            if user_input_gset == 4:
                help()
            elif user_input_gset == 1:
                gsettings_parser()
            elif user_input_gset == 2:
                gsettings_max_workers()
            elif user_input_gset == 3:
                gsettings_url()


def gsettings_parser():
    gs_parser = parser  #{1: 'bs4', 2: 'selenium'}
    print(f'{1}: {gs_parser["1"]}\n{2}: {gs_parser["2"]}')
    while True:
        try:
            user_input_lset = int(input('Введите номер парсера: '))
            if user_input_lset <= 0 or user_input_lset > 4:
                raise ValueError("Введите число соответствующее парсеру !!!")
        except ValueError as error:
            print(error)
        else:
            if parser[str(1)] == gs_parser[str(user_input_lset)]:
                start(parser)
                main()
            else:
                parser[str(1)], parser[str(2)] = gs_parser[str(2)], gs_parser[str(1)]

                with open('settings/set_parser.json', 'w', encoding='utf8') as file:
                    json.dump(parser, file, ensure_ascii=False, indent=4)
                start(parser)
                main()


def gsettings_max_workers():
    print(f'1: Кол-во синхронных частей скачивания фильма(по умолчанию {set_executor_download["max_workers_file"]})\n'
          f'2: Кол-во синхронных скачиваний серий сериалов(по умолчанию {set_executor_download["max_workers_files"]})\n')
    while True:
        try:
            user_input_lset_mw = int(input('Введите номер действия: '))
            if user_input_lset_mw <= 0 or user_input_lset_mw > 3:
                raise ValueError("Введите число соответствующее действию !!!")
        except ValueError as error:
            print(error)
        else:
            if user_input_lset_mw == 1:
                while True:
                    try:
                        user_input_lset_mw_f = int(input('Введите кол-во chunks(макс-1000): '))
                        if user_input_lset_mw_f <= 0 or user_input_lset_mw_f > 1001:
                            raise ValueError("Введите число от 0 до 1000 !!!")
                    except ValueError as error:
                        print(error)
                    else:
                        set_executor_download['max_workers_file'] = user_input_lset_mw_f
                        with open('settings/set_executor_download.json', 'w', encoding='utf8') as file:
                            json.dump(set_executor_download, file, ensure_ascii=False, indent=4)
                        print(f'Установленны значения:\n   '
                              f'-кол-во chunks: {set_executor_download["max_workers_file"]}\n    '
                              f'-кол-во синхронных скачиваний серий: {set_executor_download["max_workers_files"]}')
                        main()
            else:
                while True:
                    try:
                        user_input_lset_mw_s = int(input('Введите кол-во синхронных скачиваний серий(макс-100): '))
                        if user_input_lset_mw_s <= 0 or user_input_lset_mw_s > 100:
                            raise ValueError("Введите число от 0 до 100 !!!")
                    except ValueError as error:
                        print(error)
                    else:
                        set_executor_download['max_workers_files'] = user_input_lset_mw_s
                        with open('settings/set_executor_download.json', 'w', encoding='utf8') as file:
                            json.dump(set_executor_download, file, ensure_ascii=False, indent=4)
                        print(f'Установленны значения:\n   '
                              f'-кол-во chunks: {set_executor_download["max_workers_file"]}\n    '
                              f'-кол-во синхронных скачиваний серий: {set_executor_download["max_workers_files"]}')
                        main()


def gsettings_url():
    print('Введите новый url сайта в формате: http://zagonka27.zagonko.com/ '
          '\nВнимание!!! При коппировании url из браузера url можетбыть таким http://zagonka27.zagonko.com/9,'
          ' вводите без 9')
    while True:
        try:
            user_input_lset_url = str(input('Введите новый url: '))

        except ValueError as error:
            print(error)
        else:
            old_set_zagonka = set_zagonka
            old_url = set_zagonka['zagonka_urls']['url']
            print(old_url)
            for key in set_zagonka:
                for key_2 in set_zagonka[key]:
                    print(set_zagonka[key][key_2])
                    if type(set_zagonka[key][key_2]) is str:
                        if 'http' in set_zagonka[key][key_2]:
                            set_zagonka[key][key_2] = old_set_zagonka[key][key_2].replace(f'{old_url}',
                                                                                          f'{user_input_lset_url}')
            with open('settings/zagonka_set.json', 'w', encoding='utf8') as file:
                json.dump(set_zagonka, file, ensure_ascii=False, indent=4)
            print('Изменения настроек в файле json(глобальные настойки):')
            print(set_zagonka)
            start(parser)
            main()


def run():

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


def main():

    run()


if __name__ == '__main__':

    main()

