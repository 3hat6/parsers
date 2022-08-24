""" DocString """
import random
import sqlite3
import requests
from bs4 import BeautifulSoup

id = 1
com_id = 1
sqliteConnection = sqlite3.connect(r"C:\Users\Dell\Desktop\Comments.sqlite3")
cursor = sqliteConnection.cursor()
for j in range(1, 50):
    host = 'https://ishopmsk.ru/'
    url = 'https://ishopmsk.ru/review/'
    par = {'page': j}
    r = requests.get(url, params=par)
    soup = BeautifulSoup(r.text, 'html.parser')
    main_page = soup.find('div', {'class': 'reviews_page_container'})
    main_page = main_page.findAll('div', {'class': "reviews_item"})
    for i in range(5):
        product = main_page[i]
        meta_product = product.find('p', {'class': "name"})
        user_name = meta_product.get_text()
        product_name = product.find('a', {'class': "mod"}).get_text()
        text = str(product.find('div', {'class': "info"}).get_text())
        day = random.randint(1, 31)
        month = random.randint(1, 12)
        year = 2022
        data = str(day), str(month), str(year)
        '''         
        product = product.find('div', {'class': "mob_row"})
        product_name = product.find('p', {'class': "title"}).get_text()
        price = product.find('div', {'class': "price_container"})
        price = str(price.find('p', {'class': "new_price"}).get_text())
        price = int(price.replace(' ', '')[:-1])
        price = int(price - price * 0.18)
        price = str(price) + ' ₽.'
        info = requests.get(product_link, params=par)
        product_soup = BeautifulSoup(info.text, 'html.parser')
        full_descritpion = ""
        descriptions = product_soup.find('div', {'class': 'characteristics_information'})
        descriptions = descriptions.findAll('div', {'class': 'item'})
        # descriptions = descriptions.find('div', {'class': 'item'})
        for i in range(0, len(descriptions)):
            try:
                key = str(descriptions[i].find('div', {'class': 'property'}).get_text())
                value = str(descriptions[i].find('div', {'class': 'description'}).get_text())
                full_descritpion = full_descritpion + key.strip() + " : " + value.strip() + '\n'
            except:
                meta_key = descriptions[i].find('p').get_text()
                full_descritpion += str(meta_key)
                full_descritpion += '\n' 
        images_links = product_soup.find('div', {'class': 'product_top_container'})
        images_links = images_links.find('div', {'class': 'gallery_product'})
        images_links = (images_links.find('div', {'style': 'position:relative;'}))
        img_links = str(images_links.find_all('a')).split('\n')
        jpg_links = ""
        for elem in img_links:
            start = int(str(elem).find('href')) + 6
            end = str(elem).find('style="display') - 2
            images_links = elem[start:end]
            if images_links.endswith('jpg') & images_links.startswith('https'):
                jpg_links = jpg_links + "\n" + images_links + "\n"
        try:
            vitrine = jpg_links[jpg_links.index("\n"):].replace('max-700', 'max-228')
        except:
            pass
        # print(product_name)
        # print(price)
     
        start = int(str(images_links).find('href')) + 6
        end = str(images_links).find('style="display') - 2
        for k in range(1, 5):
            product_images = product_images + "\n" + (
                product_image.replace(product_image[-7:-4], str(int(product_image[-7:-4]) + k))) '''
        cursor.execute(
            '''INSERT INTO "iPhones" ( comment_id, user_name, text, date, "product_name(id)")
             VALUES(?,?,?,?,?,?)''', (id, com_id, user_name, text, data, product_name))
        id += 1
        vitrine = ""
        sqliteConnection.commit()




