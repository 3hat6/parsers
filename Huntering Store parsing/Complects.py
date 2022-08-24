""" DocString """

import sqlite3
import requests
from bs4 import BeautifulSoup

sqliteConnection = sqlite3.connect(r"C:\sqlite\db\hunting.sqlite3")
cursor = sqliteConnection.cursor()
data = []

for j in range(1, 150):
    host = 'https://spinningline.ru'
    url = 'https://spinningline.ru/search_by_options.php?f-apply=true&f-cid=17557&f-entry-cid=36225&f-60-select=32304&f-slider-33-min=6.30&f-slider-33-minval=6.30&f-slider-33-max=62.00&f-slider-33-maxval=62.00&f-valut-calculated=1&f-slider-33-float=2&f-slider-42-min=190.00&f-slider-42-minval=190.00&f-slider-42-max=380.00&f-slider-42-maxval=380.00&f-slider-42-float=2&f-slider-44-min=96.00&f-slider-44-minval=96.00&f-slider-44-max=179.00&f-slider-44-maxval=179.00&f-slider-44-float=2&f-slider-59-min=150&f-slider-59-minval=150&f-slider-59-max=650&f-slider-59-maxval=650&f-slider-59-float=1&f-slider-58-min=2.50&f-slider-58-minval=2.50&f-slider-58-max=30.00&f-slider-58-maxval=30.00&f-slider-58-float=2&f-slider-67-min=1&f-slider-67-minval=1&f-slider-67-max=5&f-slider-67-maxval=5&f-slider-67-float=1&f-stockin=0&f-slider-cost-min=7616&f-slider-cost-minval=7616&f-slider-cost-max=79530&f-slider-cost-maxval=79530&f-slider-cost-float=100&f-arrival=0&orderby=price.desc&page=1'
    par = {'page': j}
    r = requests.get(url, params=par)
    soup = BeautifulSoup(r.text, 'html.parser')
    products = soup.find_all('div', {'class': 'b-prod-wrap'})
    for i in range(25):
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
        characteristics_keys = ["Вес(гр)", "Вид ловли", "Диаметр переднего бортика шпули (мм)", "Класс катушки",
                                "Кнопка на рукояти",
                                "Количество подшипников", "Комплектация", "Нагрузка на фрикцион(кг)", "Объем шпули",
                                "Передаточное число",
                                "Способ крепления рукояти", "Страна изготовления", "Тип механизма", "Фрикцион",
                                "Производитель"]
        try:
            product_description = str(product_soup.find('div', {'itemprop': 'description'}).get_text())

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
            '''INSERT INTO  "Лодки, Моторы" (id, Товар, Категория, Бренд, Вариант, Цена, "Старая цена", Склад,  
                        Артикул, Видим, Рекомендуемый, Аннотация, Адрес, Описание, Изображения, "Заголовок страницы", 
                        "Ключевые слова", Производитель)  VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
            (None, product_name, "Электроника", brand, "", int(price), int(old_price), "7", "", 1, 0, '', '',
             product_description,
             links[:-2], product_name, '', characteristics["Производитель"]))
        sqliteConnection.commit()
        print(product_name, "||", product_link)
