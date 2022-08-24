""" DocString """

import sqlite3
import requests
from bs4 import BeautifulSoup

sqliteConnection = sqlite3.connect(r"C:\sqlite\db\Products.sqlite3")
cursor = sqliteConnection.cursor()
data = []

for j in range(1, 50):
    host = 'https://spb.vseinstrumenti.ru'
    url = 'https://spb.vseinstrumenti.ru/sadovaya_tehnika/vozduhoduvki/'
    par = {'page': j}
    r = requests.get(url, params=par)
    soup = BeautifulSoup(r.text, 'html.parser')
    products = soup.find_all('div', {'class': 'product-row grid-item'})
    for i in range(20):
        product = products[i].find('div', {'class': 'title'})
        product_name = product.get_text()
        start = str(product).find('href') + 6
        product_link = host + str(product)[start:]
        end = str(product_link).find('" ') - 1
        product_link = product_link[:end]
        price = products[i].find('div', {'class': 'price'}).get_text().replace(' ', '')[:-2]
        price = int(float(price) - float(price) * 0.2)
        print(price)
        print(product_link)
        info = requests.get(product_link, params=par)
        product_soup = BeautifulSoup(info.text, 'html.parser')
        try:
            product_description = product_soup.find('ul', {'class': 'product-features'}).get_text()
            product_description.replace('  ', '\n')
        except:
            product_description = ""
        images_links = product_soup.find('div', {'class': 'stage'})
        start = str(images_links).find('https')
        end = str(images_links).find('src="data:image') - 2
        product_image = str(images_links)[start:end].replace("68x60", "560x504")
        product_images = ""
        for k in range(1, 5):
            product_images = product_images + "\n" + (
                product_image.replace(product_image[-7:-4], str(int(product_image[-7:-4]) + k)))
        data.append([product_name, price, product_description, product_images])
        cursor.execute(
            '''INSERT INTO "Котлы" (name, price, description, image_links)
             VALUES(?,?,?,?)''', (product_name, price, product_description, product_images))
        sqliteConnection.commit()
