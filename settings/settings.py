import json
import re

set_zagonka = {}


def open_json_zset():

    with open('settings/zagonka_set.json', encoding='utf8') as file:  #
        par_str = file.read()
        zset = json.loads(par_str)

    return zset

set_zagonka = open_json_zset()


set_executor_download = {}


def open_set_executor_download():

    with open('settings/set_executor_download.json', encoding='utf8') as file: #
        par_str = file.read()
        ed = json.loads(par_str)
    return ed

set_executor_download = open_set_executor_download()


def new_set_zagonka(set_zagonka_old:dict, new_url:str):
    """Функция для локального изменения url сайта загонка
    Пока не используется,т.к. реализованна в файле main"""
    new_set = set_zagonka_old
    old_url = set_zagonka_old['zagonka_urls']['url']
    print(old_url)
    for key in set_zagonka:
        for key_2 in set_zagonka[key]:
            print(set_zagonka[key][key_2])
            if type(set_zagonka[key][key_2]) is str:
                if 'http' in set_zagonka[key][key_2]:
                    new_set[key][key_2] = new_set_zagonka[key][key_2].replace(f'{old_url}',
                                                                                  f'{ new_url}')
    return new_set


def new_set_zagonka_json(set_zagonka_old:dict, new_url:str):
    """Функция для глобального изменения url сайта загонка
    Пока не используется,т.к. реализованна в файле main"""
    new_set_zagonka_json = set_zagonka_old
    old_url = set_zagonka_old['zagonka_urls']['url']
    print(old_url)
    for key in set_zagonka:
        for key_2 in set_zagonka[key]:
            print(set_zagonka[key][key_2])
            if type(set_zagonka[key][key_2]) is str:
                if 'http' in set_zagonka[key][key_2]:
                    new_set_zagonka_json[key][key_2] = new_set_zagonka_json[key][key_2].replace(f'{old_url}',
                                                                                  f'{new_url}')
    with open('settings/zagonka_set.json', 'w', encoding='utf8') as file:
        json.dump(new_set_zagonka_json, file, ensure_ascii=False, indent=4)

    return new_set_zagonka_json


def auto_change_url(set_zagonka_old:dict):
    """Функция для автоматической замены url в json файле, в случае бана сайта, и последующей за этим сменой url"""
    new_set_zagonka_json = set_zagonka_old
    old_url = set_zagonka_old['zagonka_urls']['url']

    num_in_url = re.findall('(\d+)', old_url)  # =>list
    count = int(num_in_url[0])+1
    new_url = old_url.replace(f'{num_in_url[0]}', f'{str(count)}')
    for key in new_set_zagonka_json:
        for key_2 in new_set_zagonka_json[key]:
            if type(new_set_zagonka_json[key][key_2]) is str:
                if 'http' in new_set_zagonka_json[key][key_2]:
                    new_set_zagonka_json[key][key_2] = new_set_zagonka_json[key][key_2].replace(f'{old_url}',
                                                                                  f'{new_url}')
            else:
                new_set_zagonka_json[key][key_2] = count
    with open('settings/zagonka_set.json', 'w', encoding='utf8') as file:
        json.dump(new_set_zagonka_json, file, ensure_ascii=False, indent=4)

    return new_set_zagonka_json

