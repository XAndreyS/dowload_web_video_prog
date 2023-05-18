import json

set_zagonka = {}


def open_json_zset():

    with open('settings/zagonka_set.json', encoding='utf8') as file:
        par_str = file.read()
        zset = json.loads(par_str)

    return zset

set_zagonka = open_json_zset()


set_executor_download = {}


def open_set_executor_download():

    with open('settings/set_executor_download.json', encoding='utf8') as file:
        par_str = file.read()
        ed = json.loads(par_str)
    return ed

set_executor_download = open_set_executor_download()