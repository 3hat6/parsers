""" DocString """
import sqlite3
import requests
from bs4 import BeautifulSoup

sqliteConnection = sqlite3.connect(r"C:\Users\Dell\Desktop\Phones.sqlite3")
cursor = sqliteConnection.cursor()
lid = 1
for j in range(1, 50):
    host = 'https://electrotown.ru/'
    url = 'https://electrotown.ru/electrokvadrocikl/?sort=p.sort_order&order=ASC'
    par = {'page': j}
    r = requests.get(url, params=par)
    soup = BeautifulSoup(r.text, 'html.parser')
    products = soup.find('div', {'class': 'row grid-july'})
    products = products.findAll('div', {'itemtype': "http://schema.org/Product"})
    for i in range(15):
        product = products[i].find('div', {'class': "july_view5"})
        product_name = product.find('h4', {'itemprop': "name"}).get_text()
        product_link = product.find('a').get('href')
        description = str(product.find('table').get_text())
        try:
            old_price = int(product.find('span', {'class': "price-new"}).get_text().replace(' ', '')[:-2])
        except:
            old_price = int(product.find('p', {'class': "price"}).get_text().replace(' ', '')[:-2])
        price = int(old_price - old_price * 0.40)
        info = requests.get(product_link, params=par)
        product_soup = BeautifulSoup(info.text, 'html.parser')
        product_info_page = product_soup.find('div', {'class': 'row product-info'})
        descriptions = product_info_page.find('table', {'class': 'table table-bordered'})
        descriptions = descriptions.findAll('tr')
        characteristics = {}
        all_list = {}
        for k in range(1, len(descriptions)):
            elems = descriptions[k].findAll('td')
            key = str(elems[0].get_text())
            if key == 'Дополнительно':
                continue
            value = str(elems[1].get_text())
            characteristics[key] = value

        characteristics_keys = ["Размер колес", "Скорость", "Расстояние", "Вес водителя", "Мощность", "Время зарядки",
                                "Батарея", "Амортизация", "Рама", "Тормоза", "Вес", "Дисплей", "Фары", "Сидение",
                                "Подножка", "Приложение APP"]

        for char_key in characteristics_keys:
            if char_key not in characteristics.keys():
                characteristics[char_key] = None
        try:
            small_description = product_info_page.find('div', {'id': 'tab-description'}).find('p').get_text() + '\n'
        except:
            small_description = ''
        jpg_links = ""
        try:
            images_links = product_info_page.find('div', {'class': 'carousel-inner'})
            images_links = images_links.findAll('a')
            for v in range(len(images_links)):
                jpg_links = jpg_links + images_links[v].get("data-zoom-image") + ', '
        except:
            print("error", product_name, "||", product_link)

        comments = product_info_page.find('div', {'id': 'review'}).findAll('table', {'class': 'table'})
        for comm in comments:
            comm_author = (comm.find('strong', {'itemprop': 'author'}).get_text())
            comm_text = (comm.find('p', {'itemprop': 'reviewBody'}).get_text())
        cursor.execute(
            '''INSERT INTO "Электроквадроциклы" (id, Товар, Категория, Бренд, Вариант, Цена, "Старая цена", Склад, Артикул, 
                Видим, Рекомендуемый, Аннотация, Адрес, Описание, Изображения, "Заголовок страницы", "Ключевые слова", 
                "Размер колес", Скорость, Расстояние, "Вес водителя", Мощность, "Время зарядки", Батарея, 
                Амортизация, Рама, Тормоза, Вес, Дисплей, Фары, Сидение, Подножка, 'Приложение APP') 
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
            (None, product_name, "Электроскутеры", "", "", price, old_price, "7", "", 1, 0, '', '',
             small_description, jpg_links[:-2], product_name, '', characteristics["Размер колес"],
             characteristics["Скорость"], characteristics["Расстояние"], characteristics["Вес водителя"],
             characteristics["Мощность"], characteristics["Время зарядки"], characteristics["Батарея"],
             characteristics["Амортизация"], characteristics["Рама"], characteristics["Тормоза"],
             characteristics["Вес"], characteristics["Дисплей"], characteristics["Фары"], characteristics["Сидение"],
             characteristics["Подножка"], characteristics["Приложение APP"]))
        sqliteConnection.commit()
        print(lid, product_name, "||", product_link)
        lid += 1
