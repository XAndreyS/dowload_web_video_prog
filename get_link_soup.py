import requests
from bs4 import BeautifulSoup
import time
from collections import defaultdict
import json


class ZagonkaSoup():
    def __init__(self):
        pass

    def searh_zagoka(url, search):

        url = url
        cookies = {
            '_ga': 'GA1.1.731450299.1682421306',
            '_ga_X6M5R33EXW': 'GS1.1.1682710055.6.1.1682710377.0.0.0',
            'PHPSESSID': '4f9da1063ee9b85e8ceeb127f27c4a74',
            '_ga_P1K99CP13B': 'GS1.1.1682775593.7.1.1682775597.0.0.0',
        }

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            # 'Cookie': '_ga=GA1.1.731450299.1682421306; _ga_X6M5R33EXW=GS1.1.1682710055.6.1.1682710377.0.0.0; PHPSESSID=4f9da1063ee9b85e8ceeb127f27c4a74; _ga_P1K99CP13B=GS1.1.1682775593.7.1.1682775597.0.0.0',
            'Referer': 'http://zagonko22.zagonko.com/9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'X-KL-kfa-Ajax-Request': 'Ajax_Request',
            'X-Requested-With': 'XMLHttpRequest',
        }

        params = {
            'q': f'{search}',
        }

        response = requests.get(
            url=url,
            params=params,
            cookies=cookies,
            headers=headers,
            verify=False,
        )

        return response.json()

    def get_url_content(res_dict: dict):
        return res_dict['url']

    def get_name_content(res_dict: dict):
        return res_dict['text']

    def get_link_content(url='', url_content=''):

        cookies = {
            '_ga': 'GA1.1.731450299.1682421306',
            '_ga_X6M5R33EXW': 'GS1.1.1682710055.6.1.1682710377.0.0.0',
            'PHPSESSID': '4f9da1063ee9b85e8ceeb127f27c4a74',
            '_ga_P1K99CP13B': 'GS1.1.1682775593.7.1.1682775597.0.0.0',
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            # 'Cookie': '_ga=GA1.1.731450299.1682421306; _ga_X6M5R33EXW=GS1.1.1682710055.6.1.1682710377.0.0.0; PHPSESSID=4f9da1063ee9b85e8ceeb127f27c4a74; _ga_P1K99CP13B=GS1.1.1682775593.7.1.1682775597.0.0.0',
            'Referer': 'http://zagonko22.zagonko.com/9',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }

        response = requests.get(
            url=url+url_content,
            cookies=cookies,
            headers=headers,
            verify=False,
        )
        return response.text

    def get_kpid(res_html):

        soup = BeautifulSoup(res_html, 'html.parser')
        find_kpid = soup.find('div', id='player')

        return find_kpid['data-kp']

    def get_id(res_dict: dict):
        return res_dict['id']

    def get_down_html(id: str, kpid: str):
        cookies = {
            '_ga': 'GA1.1.731450299.1682421306',
            'PHPSESSID': '4f9da1063ee9b85e8ceeb127f27c4a74',
            '_ga_P1K99CP13B': 'GS1.1.1682775593.7.1.1682775967.0.0.0',
            '_ga_X6M5R33EXW': 'GS1.1.1682775982.7.0.1682776016.0.0.0',
        }

        headers = {
            'Accept': 'application/xml, text/xml, */*; q=0.01',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'Cookie': '_ga=GA1.1.731450299.1682421306; PHPSESSID=4f9da1063ee9b85e8ceeb127f27c4a74; _ga_P1K99CP13B=GS1.1.1682775593.7.1.1682775967.0.0.0; _ga_X6M5R33EXW=GS1.1.1682775982.7.0.1682776016.0.0.0',
            'Origin': 'http://zagonko22.zagonko.com',
            'Referer': 'http://zagonko22.zagonko.com/50963-15_pacany-onlayn.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'X-KL-kfa-Ajax-Request': 'Ajax_Request',
            'X-Requested-With': 'XMLHttpRequest',
        }

        data = {
            'id': id,
            'kpid': kpid
        }

        response = requests.post(
            'http://zagonko22.zagonko.com/engine/ajax/down.php',
            cookies=cookies,
            headers=headers,
            data=data,
            verify=False,
        )
        res_html = response.text.split('CDATA[')
        response_html = res_html[1].split('<style>')[0]
        return response_html

    def get_link_serial(res_html):
        tag_a_all = []
        # Модуль collections Для создания ключей и списков в значениях словаря
        #name_translater = defaultdict(lambda: defaultdict(list))
        sezons = defaultdict(lambda: defaultdict(list))
        name_translater = {}
        soup = BeautifulSoup(res_html, 'lxml')
        soup_prettify_ = soup.prettify()
        soup_find = BeautifulSoup(soup_prettify_,'lxml')
        sezons_number_list_ = soup.find('body')

        find_sezons = sezons_number_list_.find_all(class_='dspoiler',recursive=False)
        count_tanslater_dict = {}
        count_sezons = len(find_sezons)
        # Получаем словарь счётчик,  где ключ это №сезона, значение кол-во переводов
        for c in range(1, count_sezons + 1):
            count_tanslater_dict[f'{c}'] = len(find_sezons[c-1].find_all(class_="dspoiler"))
        count = 0  # Общий сётчик

        for key in count_tanslater_dict:
            find_translaters_sezon = find_sezons[count].find(class_='mfs')
            name_translater[str(count + 1)] = find_translaters_sezon.text
            if count_tanslater_dict[key] > 1:
                for i in range(0,count_tanslater_dict[key]):
                    tag_a_240 = []
                    tag_a_360 = []
                    tag_a_480 = []
                    find_a = []
                    for a_h in find_sezons[count].select(f".dspoiler:nth-of-type({i+1})"):
                        find_a = a_h.find_all('a')
                    for a in find_a:  # Цикл для упорядочивания видео по качеству
                        if a['href'][-7] == '2':
                            tag_a_240.append(a['href'])
                        elif a['href'][-7] == '3':
                            tag_a_360.append(a['href'])
                        elif a['href'][-7] == '4':
                            tag_a_480.append(a['href'])
                        tag_a_all = tag_a_240, tag_a_360, tag_a_480
                    sezons[key][i+1].append(tag_a_all)

            else:
                tag_a_240 = []
                tag_a_360 = []
                tag_a_480 = []
                find_translater = find_sezons[count].find_all('a')

                for a in find_translater:  # Цикл для упорядочивания видео по качеству
                    if a['href'][-7] == '2':
                        tag_a_240.append(a['href'])
                    elif a['href'][-7] == '3':
                        tag_a_360.append(a['href'])
                    elif a['href'][-7] == '4':
                        tag_a_480.append(a['href'])
                    tag_a_all = tag_a_240, tag_a_360, tag_a_480
                find_translater.clear()
                sezons[str(count+1)][1].append(tag_a_all)
            count += 1
        #with open('dick_serial_soup.json', 'w', encoding='utf8') as file:
        #    json.dump(sezons, file, ensure_ascii=False, indent=4)
        return sezons,name_translater

    def get_link_film(res_html, name_film: str):

        # Модуль collections Для создания ключей и списков в значениях словаря
        film_link = defaultdict(lambda: defaultdict(list))
        translater_dict = {}
        name_film = name_film.split('(')[0].strip()
        soup = BeautifulSoup(res_html, 'lxml')
        soup_prettify_ = soup.prettify()
        soup_find = BeautifulSoup(soup_prettify_, 'lxml')
        film_translater_list_html = soup.find_all(class_="in_tr")  # Список переводов для фильма
        link_translater_list_html = soup.find_all(class_="dbord")  # Локатор на тег а по переводам
        # Счетчик имен
        count_name = 1
        for name in film_translater_list_html:
            translater_dict[count_name] = name.text
            count_name += 1
        # Счетчик перееводов
        count_translater = 1

        for links in link_translater_list_html:
            tag_a_html = links.find_all('a')

            # Цилк по веб элементам с ссылками, достаем  знамение аттрибута href
            for a in tag_a_html:
                # Проблема с добавлением отдельного списка ссылок по качеству в  отдеельный ключ,
                # пока решено с помощью Модуль collections
                film_link[name_film][count_translater].append(a['href'])
            count_translater += 1

        return film_link, translater_dict


def main():
    url_zagonka = 'http://zagonko22.zagonko.com/'
    user_search = input('Введите название фильма/сериала: ')
    data_serch_list = ZagonkaSoup.searh_zagoka('http://zagonko22.zagonko.com/engine/ajax/xsearch/f.php', user_search)
    count = 1
    for content in data_serch_list:
        print(f"{count}: {content['text']}")
        count += 1
    user_num_content = input('Введите номер фильма/сериала: ')

    url_content = ZagonkaSoup.get_url_content(data_serch_list[int(user_num_content)-1])
    name_content = ZagonkaSoup.get_name_content(data_serch_list[int(user_num_content)-1])
    res_html = ZagonkaSoup.get_link_content(url_zagonka, url_content)
    id_content = ZagonkaSoup.get_id(data_serch_list[int(user_num_content)-1])
    kpid_content = ZagonkaSoup.get_kpid(res_html)
    down_html = ZagonkaSoup.get_down_html(id_content, kpid_content)
    link_film = ZagonkaSoup.get_link_film(down_html,name_content)
    #get_link_serial(down_html)
    print(link_film)

if __name__ == '__main__':

    main()

