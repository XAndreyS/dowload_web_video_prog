#import Selenium

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from collections import defaultdict


class Serial():
    def __init__(self):
        pass

    def data__serial(count_sezons:int, web_element):
        """Сбор и упорядочивание информации
        Вход count_sezons:int - кол-восезонов, web_element - веб элемент Селениум.
        Результат:
        Получаем множество: словарь с количеством переводов в сезоне и ссылками на скаивание
        и словарь с именами переводов(если в сезоне болеее одно перевода, по какой то причине
        не получается вытащить текст из локатора, пока решено "костылём")
        """
        count_sezons = count_sezons
        web_element = web_element

        count_tanslater_dict = {}
        name_translater = {}
        # Получаем словарь счётчик,  где ключ это №сезона, значение кол-во переводов
        for c in range(1, count_sezons + 1):
            count_tanslater_dict[f'{c} Сезон'] = len(web_element[1].find_elements(By.XPATH, f'//div[@id="down"]'
            f'/div[@class="dspoiler"][{c}]/div[@class="d_cont"]/div[@class="dspoiler"]'))

        count = 1  # Общий сётчик
        # Модуль collections Для создания ключей и списков в значениях словаря
        name_translater = defaultdict(lambda: defaultdict(list))
        sezons = defaultdict(lambda: defaultdict(list))
        # Цикл по словарю счётчику
        for key in count_tanslater_dict:
            #  Если в сезоне переводов более одного
            if count_tanslater_dict[key] > 1:
                #  Получччаем Данные попереводам в сезоне(покаа будут отдельным словарем)
                find_tanslaters_sezon = web_element[1].find_element(By.XPATH, f'//div[@id="down"]'
                f'/div[@class="dspoiler"][{count}]/div[@class="dtitle"]/div[@class="in_s"]/div[@class="mfs"]')
                name_translater[count]=find_tanslaters_sezon.text # .replace("(", "").split(")")
                #  Цикл проходим по кол-ву переводов в сезоне
                for i in range(count_tanslater_dict[key]):
                    tag_a_240 = []
                    tag_a_360 = []
                    tag_a_480 = []
                    #  Получаем веб элементы со ссылками на видео
                    tag_a_html = web_element[1].find_elements(By.XPATH, f'//div[@id="down"]/div[@class="dspoiler"]'
                    f'[{count}]/div[@class="d_cont"]/div[@class="dspoiler"][{i+1}]//a')
                    for a in tag_a_html:  # Цикл для упорядочивания видео по качеству
                        if a.get_attribute('href')[-7] == '2':
                            tag_a_240.append(a.get_attribute('href'))
                        elif a.get_attribute('href')[-7] == '3':
                            tag_a_360.append(a.get_attribute('href'))
                        elif a.get_attribute('href')[-7] == '4':
                            tag_a_480.append(a.get_attribute('href'))
                        tag_a_all = tag_a_240, tag_a_360, tag_a_480
                    # Записываем в словарь номера сезонов, кол-во переводов и ссылки на видео для каждого
                    sezons[key][i+1].append(tag_a_all)
            else:  # Если в сезоне один первод
                find_tanslater_sezon = web_element[1].find_element(By.XPATH, f'//div[@id="down"]'
                f'/div[@class="dspoiler"][{count}]/div[@class="dtitle"]/div[@class="in_s"]/div[@class="mfs"]')
                name_translater[count] = find_tanslater_sezon.text  # .replace("(", "").split(")")
                tag_a_240 = []
                tag_a_360 = []
                tag_a_480 = []
                #  Получаем веб элементы со ссылками на видео
                tag_a_html = web_element[1].find_elements(By.XPATH, f'//div[@id="down"]/div[@class="dspoiler"]'
                f'[{count}]//a')
                for a in tag_a_html:  # Цикл для упорядочивания видео по качеству
                    if a.get_attribute('href')[-7] == '2':
                        tag_a_240.append(a.get_attribute('href'))
                    elif a.get_attribute('href')[-7] == '3':
                        tag_a_360.append(a.get_attribute('href'))
                    elif a.get_attribute('href')[-7] == '4':
                        tag_a_480.append(a.get_attribute('href'))
                    tag_a_all = tag_a_240, tag_a_360, tag_a_480
                # Записываем в словарь номера сезонов, имя перевода и ссылки на видео
                sezons[key][web_element[1].find_element(By.XPATH, f'//div[@id="down"]/div[@class="dspoiler"]'
                f'[{count}]//div[@class="in_s"]/div[@class="mfs"]').text].append(tag_a_all)

            count += 1  # Счетчик для смены сезонов в локторах

        return sezons, name_translater

    def get_link(url=''):
        """Сбор данных(ссылки на видео, названия) с сайта, с помощью селениум веб-драйвер:
        Кликаем на элемент для получения локаторов с данными для скачивания видео.
        Собираем данныескол-вом сезонов, отправляем в функцию data_find_count_sesons,
        получаем результат"""
        print('Запускаю программу')
        """Получает ссылки на видео и их имена"""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('----window-size=1400,1000')
        driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)

        driver.get(url)

        try:
            # Поиск локатора "поисковой строки"
            search_html = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input')))
        except TimeoutException:
            print('Поисковая строка не найдена')
        # Ввод пользователя названия фильма/сериала, если запрос не найден требеутся повторить ввод
        #
        # (пока это определяется ожиданием локатора "всплывающего списка" с подходящими видео по запросу)
        while True:
            try:
                search_html.send_keys(str(input('Введите название сериала/фильма:')))
                search_names_html = WebDriverWait(driver, 10).until((
                    EC.presence_of_all_elements_located((By.XPATH, '//li[@class="select2-results__option"]'))
                ))
            except TimeoutException:
                print("По зпросу ничего не найдено:")
                search_html.clear()
            else:
                break

        count_name = 1  # Счетчик для нумерации найденых видео
        print('По вашему запросу найдено')
        for name in search_names_html:
            print(f'{count_name}:{name.text}')  # Результат на экран
            count_name += 1
        try:
            # Выбор контента путем ввода его номера на экране
            # Требуется добавить исключения  для отлова некорректного ввода
            get_count = int(input('Введите номер фильма/сериала:'))
        except TimeoutException:
            print('Не верный ввод')
        else:
            search_names_html[get_count-1].click()  # Клик по выбранному контенту
            time.sleep(1)
            url_film = driver.current_url  # Получаем ссылку контента
        # Переход на страницу выбранного контента
        driver.get(url=url_film)
        try:
            click_button_html = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "down"))).click()  # клик открывающий доступ к ссылкам
            time.sleep(1)
        except TimeoutException:
            print("время ожидания кнопки скачать вышло")
            driver.close()
            driver.quit()
        try:
            # Проверяем заголовок страницы с контентом, если вназвании есть слово "сериал",
            # то запрос к функции поиска и сбора данных для сериалов,
            # иначе запрос к функции поиска и сбора данных для фидльмов.Отличаюся локаторы
            html_name = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,'//h1[@class="fll"]'))
            )
            if 'сериал' in html_name.text:
                print('собираю данные, приблизительное время ожидания 30 секунд')
                # Кол-во сезонов
                sezons_count_html = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//div[@id="down"]/div[@class="dspoiler"]')))
                sezons_count = len(sezons_count_html)

                # Результат работы функции по сбору и упорядочиванию информации
                data = Serial.data__serial(sezons_count, sezons_count_html)


                time.sleep(1)
            else:
                print('Локаторы фильмов покаа не реализованны')
        except TimeoutException:
            print("время ожидания локатора скачать вышло")
            driver.close()
            driver.quit()

        time.sleep(1)
        driver.close()
        driver.quit()
        print('Данные собраны')
        return data


def main():
    print(Serial.get_link('http://zagonka1.zagonkov.gb.net/'))


if __name__ == '__main__':
    main()
