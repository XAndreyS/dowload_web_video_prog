import requests
import json
import datetime
import time
import concurrent.futures
from concurrent.futures import as_completed
from tqdm import tqdm
import os


def executor_download_serial_sel(url_list: list, video_resolution: int, count_series: list):
    """Асинхнонное скачивание файлов(сериалы)"""
    url_list_all = url_list
    response_list = []
    count_series = count_series
    url_list_for_get = []
    # Получаем список url серий,которые выбрал пользователь и передаём его в concurrent.futures.ThreadPoolExecutor
    for count_url in range(count_series[0], count_series[1] + 1):
        url_list_for_get.append(url_list[0][video_resolution - 1][count_url - 1])

    def download(url, count, timeout=20,):
        """Функция скачивания"""
        try:
            response = requests.get(url=url, stream=True)
            size = 0
            with open(f'{count} Серия.mp4', 'wb') as file:
                with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                    jobs_one = [executor.submit(download, url_list_for_get[i], i + 1) for i in
                                range(len(url_list_for_get))]
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        size += file.write(chunk)
            return size
        except Exception as ex:
            return 'Upps Eror'

    #for res in url_list_for_get:
    #    response = requests.get(res, stream=True)
    #    file_size = int(response.headers.get('content-length', 0))
    #    response_list.append(file_size)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        jobs_all = [executor.submit(download, url_list_for_get[i], i+1) for i in range(len(url_list_for_get))]

        with tqdm(unit='iB', unit_scale=True, unit_divisor=1024 * 1024, leave=True, colour='cyan') as bar:  #total=file_size
            for job in as_completed(jobs_all):
                size = job.result()
                bar.update(size)


def executor_download_film(url_list: list, video_resolution: int, film_name: str):
    """Асинхнонное скачивание файла(фильмы)
    не мой код"""
    print(f'Скачивание началось!!!!!!!\n============')

    def download_part(url_and_headers_and_partfile):
        url, headers, partfile = url_and_headers_and_partfile
        response = requests.get(url, headers=headers)
        # setting same as below in the main block, but not necessary:
        chunk_size = 1024 * 1024

        # Need size to make tqdm work.
        size = 0
        with open(partfile, 'wb') as f:
            for chunk in response.iter_content(chunk_size):
                if chunk:
                    size += f.write(chunk)
        return size

    def make_headers(start, chunk_size):
        end = start + chunk_size - 1
        return {'Range': f'bytes={start}-{end}'}

    url_list = url_list
    video_resolution = video_resolution
    film_name = film_name.split("(")[0]
    url = url_list[video_resolution - 1]
    count = 0
    file_name = f'{film_name}.mp4'
    response = requests.get(url, stream=True)
    file_size = int(response.headers.get('content-length', 0))
    chunk_size = 1024 * 1024
    chunks = range(0, file_size, chunk_size)
    my_iter = [[url, make_headers(chunk, chunk_size), f'{file_name}.part{i}'] for i, chunk in enumerate(chunks)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        jobs = [executor.submit(download_part, i) for i in my_iter]

        with tqdm(total=file_size, unit='iB', unit_scale=True, unit_divisor=chunk_size, leave=True,
                  colour='cyan') as bar:
            for job in as_completed(jobs):
                size = job.result()
                bar.update(size)

    with open(file_name, 'wb') as outfile:
        for i in range(len(chunks)):
            chunk_path = f'{file_name}.part{i}'
            with open(chunk_path, 'rb') as s:
                outfile.write(s.read())
            os.remove(chunk_path)


def executor_download_serial_soup(url_list: list, video_resolution: int, count_series: list):
    """Асинхнонное скачивание файлов(сериалы)"""
    url_list_all = url_list
    response_list = []
    https = 'https:'
    count_series = count_series
    url_list_for_get = []
    # Получаем список url серий,которые выбрал пользователь и передаём его в concurrent.futures.ThreadPoolExecutor
    for count_url in range(count_series[0], count_series[1] + 1):
        url_list_for_get.append(url_list[0][video_resolution - 1][count_url - 1])

    def download(url, count, timeout=20,):
        """Функция скачивания"""
        try:
            response = requests.get(url=url, stream=True)
            size = 0
            with open(f'{count} Серия.mp4', 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        size += file.write(chunk)
            return size
        except Exception as ex:
            return 'Upps Eror'

    for res in url_list_for_get:
        response = requests.get(https+res, stream=True)
        file_size = int(response.headers.get('content-length', 0))
        response_list.append(file_size)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        jobs_all = [executor.submit(download, url_list_for_get[i], i+1) for i in range(len(url_list_for_get))]

        #with tqdm(total=file_size,unit='iB', unit_scale=True, unit_divisor=1024 * 1024, leave=True, colour='cyan') as bar:  #total=file_size
        #    for job in as_completed(jobs_all):
        #        size = job.result()
        #        print(f'SSSSSS+++++++++{size}')
        #        bar.update(size)

def main():
    pass
    #executor_download_serial(url_list=url_list,video_resolution=video_resolution,count_series=count_list)


if __name__ == '__main__':
    main()




