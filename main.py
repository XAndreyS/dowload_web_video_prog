import requests
import json
import datetime
import time
from download_video import downloads_serial_soup, downloads_film, downloads_content
from download_video_async import executor_download_film, executor_download_serial_soup
from get_link_sel import Serial
from user_terminal_soup import run_user_terminal


def main():
    print('Достуные сайты для скачивания видео:')
    print('1) Загонка')
    print('2) другое')
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
        run = run_user_terminal()
    else:
        while True:
            try:
                user_input_url = str(input('Введите cссылку на видео: '))
            except ValueError as error:
                print(error)
            else:
                break
        downloads_content(user_input_url)


if __name__ == '__main__':

    main()


# https://www.tiktok.com/@babycoma13/video/6960334367952489729?is_from_webapp=1&sender_device=pc