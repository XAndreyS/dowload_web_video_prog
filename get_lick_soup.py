import Selenium

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import time


serial = {}
#sezons_list = []
sezons = []
sezons_count = 0
#sezons_count = 1
#sezons_number = []
sezons_translater = []
#perevod = []
#names_series = []
#series_link = []
links_video_240 = {}
links_video_360 = {}
links_video_480 = {}
#links_video_list_all = []
#lincks_list_dick = []



#a = []

class Get_Link():

    def get_linck(url):
        """Открывает доступ к данным после клика с помощью селениум веб-драйвер"""
        print('собираю данные')
        """Получает ссылки на видео и их имена"""
        driver = webdriver.Chrome(executable_path='chromedriver.exe')
        driver.set_window_size(1400, 1000)
        driver.get(url)

        try:
            click_button_html = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "down"))).click()  # клик открывающий доступ к ссылкам
            time.sleep(3)
        except TimeoutException:
            print("время ожидания кнопки скачать вышло")
            driver.close()
            driver.quit()
        try:
            page = driver.page_source
            time.sleep(2)
        except TimeoutException:
            print("время ожидания локатора скачать вышло")
            driver.close()
            driver.quit()
        time.sleep(1)
        driver.close()
        driver.quit()

        return page

    def get_data(page):
        """Получить данные страницы впомощью bs4"""
        soup = BeautifulSoup(page, 'html.parser')  # 'lxml'
        sezons_number_list_ = soup.find(id='down')
        with open("html_serial.txt", 'w', encoding="utf=8") as myFile:
            print(sezons_number_list_.prettify(), file=myFile)
        #sezons_number_list_first = sezons_number_list_.find_next( class_='dspoiler') # Первый сезон
        # Последующие сезоны
        #sezons_number_list_next = sezons_number_list_first.find_next_siblings(class_='dspoiler')

        #count_sezons = 1
        #for i in range(len(sezons_number_list_next)+1): #  Определяем кол-во сезонов
        #    count_sezons += 1
        #    sezons.append(f'{count_sezons} Сезон')
        #sezons_translater_ = sezons_number_list_first.find_all(class_="in_tr")  # Список переводов первого сезона
        #for translater in range(len(sezons_translater_)):
        #    # Записываем имена передовов  первого сезона в глобальный список
        #    serial[f'translater_S1_{translater+1}'] = sezons_translater_[translater].text
        count_sezons = 1
        sezons_next_ = []
        sezons_next_link = []
        sezons_number_list_all = sezons_number_list_.find_all(class_='dspoiler',recursive=False)
        names_series=[]
        for i in range(len(sezons_number_list_all)):
            names_series.append(sezons_number_list_.select('.d_cont .in_e'))
            sezons_next_link.append(sezons_number_list_all[i].find_all(class_="d_cont"))
            # Если переводов более одного,то class_="in_tr",иначе class_="in_tr"
            sezons_next_.append(sezons_number_list_all[i].find_all(class_="in_tr")) # Если переводов более одного
            if sezons_next_[i] is not True:
                sezons_next_.pop(i) #  Удаляем пустой элемент списка
                sezons_next_.append(sezons_number_list_all[i].find_all(class_="in_s"))

        sezons_all = []
        sezons_link_video_ = []
        links_video = []
        sezons_link_video = {}
        link_html_soup = []


        for i in range(len(sezons_next_link)):
            for j in sezons_next_link[i]:
                sezons_link_video_.append(j.find_all('a'))
                sezons_all.append(j.find_all(class_='in_e'))
        for i in names_series:
            for j in i:

                print (f'+++++{i}')
        #print (len(sezons_link_video_[6]))
        #for i in range(len(sezons_link_video_)):
        #    #if i == 0 or i == 1:
        #        #print (sezons_link_video_[i])#
        #    print (len(sezons_all[i]))
        #    for j in sezons_all[i]:
        #        print (j.text)
            #print (len(sezons_link_video_[i]))
        #print (sezons_all)
        #print (sezons_link_video_)
        count_tanslater = 111
        for i in sezons_link_video_:
            for j in i:
                links_video.append(j.get('href'))
        #print (sezons_link_video)
        print (len(sezons_next_link))
        print (sezons_next_)
        return 'Собраны номера сезонов\nСобраны названия переводов посезонам'

        #print (sezons_number_list_first.prettify())







def data_dick(links_list):
    """Упорядычивает ссылки на видео по качеству из списка в словарь """
    print('Начинаю упорядычивание данных')
    #print(links_list)
    count_240 = 1
    count_360 = 1
    count_480 = 1
    for i in links_list:
        if i[-7] == '2':
            links_video_240[f'{count_240} Серия'] = i
            count_240 += 1
        elif i[-7]== '3':
            links_video_360[f'{count_360} Серия'] = i
            count_360 += 1
        elif i[-7] == '4':
            links_video_480[f'{count_480} Серия'] = i
            count_480 += 1
    return 'Упорядычивание завершеено' #links_video_240,links_video_360,links_video_480


def main():
    #print(Get_Link.get_linck('http://zagonka1.zagonkov.gb.net/37239-1_geroi-onlayn.html#play_video'))
    page = Get_Link.get_linck('http://zagonka1.zagonkov.gb.net/37239-1_geroi-onlayn.html#play_video')
    print(Get_Link.get_data(page))
    #data_dick(links_video_list_all)
    #print(f'Видеео 240:\n{links_video_240}\n'
    #      f'\nВидео 360:\n{links_video_360}\n'
    #      f'\nВидео 480:\n{links_video_480}')

    #print(sezons_list_ )
    #print(sezons_list)
    #print(sezons_number)


if __name__ == '__main__':
    main()