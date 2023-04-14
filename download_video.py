import requests
import json
import datetime
import time


def downloads(url_list, video_resolution, count_series):
    count_in = 1
    count_out = count_series[1]
    print(f'Скачивание началось!!!!!!!\nВсего для скачивания {count_out} видео\n============')
    try:
        for count_url in range(count_series[0], count_series[1]+1):
            t_new = datetime.datetime.now()
            response = requests.get(url=url_list[0][video_resolution-1][count_url-1])
            print(f'Скачивается {count_in} видео файл')
            with open(f'{count_url}_seria.mp4', 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        file.write(chunk)
            print (f'Время скаччивания файла:{datetime.datetime.now() - t_new}')
            print(f'Осталось скачать {count_out-1} видео файл/файлов')
            count_in += 1
            count_out -= 1
        return 'Video download'
    except Exception as ex:
        return 'Upps Eror'


def main():
    pass


if __name__ == '__main__':
    main()