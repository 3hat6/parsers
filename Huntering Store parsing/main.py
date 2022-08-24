""" DocString """

import sqlite3
import requests
from bs4 import BeautifulSoup

sqliteConnection = sqlite3.connect(r"C:\sqlite\db\hunting.sqlite3")
cursor = sqliteConnection.cursor()
data = []

for j in range(1, 150):
    host = 'https://spinningline.ru'
    url = 'https://spinningline.ru/udilishcha-c-8095.html?orderby=price.desc&allproducts=true'
    par = {'page': j}
    r = requests.get(url, params=par)
    soup = BeautifulSoup(r.text, 'html.parser')
    products = soup.find_all('div', {'class': 'b-prod-wrap'})
    for i in range(20):
        product = products[i].find('div', {'class': 'b-prod'})
        brand = product.find('meta', {'itemprop': 'brand'}).get('content')
        product_name = product.find('div', {'class': 'b-prod__name'})
        product_link = product_name.find('a', {'itemprop': 'url'}).get('href')
        product_link = host + product_link
        product_name = str(product_name.text).strip()
        price = product.find('span', {'itemprop': 'priceCurrency'}).get_text().replace(' ', '').strip()[:-2]
        old_price = float(price)
        price = old_price - float(price) * 0.15
        info = requests.get(product_link, params=par)
        product_soup = BeautifulSoup(info.text, 'html.parser')
        characteristics = {}
        about_product = product_soup.find('div', {'class': 'prod-descr-props-tr'})
        characteristics_keys = ["Вес(гр)", "Вид ловли", "Длина рукояти(см)", "Длина(см)",
                                "Класс удилища", "Количество секций", "Материал", "Рукоять", "Страна изготовления",
                                "Тест по леске (lb)", "Тест(гр)", "Тип вершинки", "Тип соединения колен",
                                "Транспортная длина (см)", "Фурнитура", "Страна изготовления"]
        try:
            product_description = str(product_soup.find('div', {'itemprop': 'description'}).get_text()).strip()

        except:
            product_description = ""
        about_product = product_soup.find('div', {'class': 'product-props'})
        keys = about_product.findAll('span', {'itemprop': 'name'})
        values = about_product.findAll('span', {'itemprop': 'value'})
        for u in range(len(keys)):
            characteristics[keys[u].text] = values[u].text
        for key in characteristics_keys:
            if key not in characteristics.keys():
                characteristics[key] = ''
        links = ""
        try:
            images = product_soup.find('div', {'class': 'prod-img-block'})
            images_links = images.findAll('img', {'itemprop': 'image'})
            for link in images_links:
                link = link.get('src')
                links = links + link + ', '
        except:
            pass
        cursor.execute(
            '''INSERT INTO Удилища (id, Товар, Категория, Бренд, Вариант, Цена, "Старая цена", Склад, Артикул, 
                            Видим, Рекомендуемый, Аннотация, Адрес, Описание, Изображения, "Заголовок страницы", 
                            "Ключевые слова", "Вес(гр)", "Вид ловли", "Длина рукояти(см)", "Длина(см)",
                             "Класс удилища", "Количество секций", Материал, Рукоять, "Страна изготовления",
                             "Тест по леске (lb)", "Тест(гр)", "Тип вершинки", "Тип соединения колен",
                            "Транспортная длина (см)", Фурнитура,  "Страна изготовления")
                             VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
            (None, product_name, "Удилища", brand, "", int(price), int(old_price), "7", "", 1, 0, '', '',
             product_description,
             links[:-2], product_name, '', characteristics["Вес(гр)"],
             characteristics["Вид ловли"], characteristics["Длина рукояти(см)"], characteristics["Длина(см)"],
             characteristics["Класс удилища"], characteristics["Количество секций"],
             characteristics["Материал"], characteristics["Рукоять"], characteristics["Страна изготовления"],
             characteristics["Тест по леске (lb)"], characteristics["Тест(гр)"], characteristics["Тип вершинки"],
             characteristics["Тип соединения колен"], characteristics["Транспортная длина (см)"],
             characteristics["Фурнитура"], characteristics["Страна изготовления"]))
        sqliteConnection.commit()
        print(product_name, "||", product_link)
