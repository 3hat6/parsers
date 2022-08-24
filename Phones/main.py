""" DocString """
import sqlite3
import requests
from bs4 import BeautifulSoup

sqliteConnection = sqlite3.connect(r"C:\Users\Dell\Desktop\Phones.sqlite3")
cursor = sqliteConnection.cursor()
for j in range(1, 50):
    host = 'https://ishopmsk.ru/'
    url = 'https://ishopmsk.ru/smartphones_iphone/'
    par = {'page': j}
    r = requests.get(url, params=par)
    soup = BeautifulSoup(r.text, 'html.parser')
    products = soup.find('div', {'class': 'category_box_position'})
    products = products.findAll('div', {'class': "card_product"})
    characteristics = ["Версия ОС на начало продаж", "Емкость аккумулятора", "Количество SIM-карт", "Размеры (ШxВxТ)",
                       "Тип SIM-карты", "Управление", "Процессор", "Размер изображения", "Диагональ",
                       "Диафрагмы основных (тыловых) камер", "Макс. разрешение видео",
                       "Разрешения основных (тыловых) камер", "Функция беспроводной зарядки",
                       "Аудио", "Вес", "Датчики"]
    all_list = {}
    characteristics = dict(zip(characteristics, [None] * len(characteristics)))
    for i in range(18):
        product = products[i]
        meta_product = product.find('a', {'class': "image_overlay"})
        product_link = meta_product.get('href')
        product = product.find('div', {'class': "mob_row"})
        product_name = str(product.find('p', {'class': "title"}).get_text())
        try:
            product_name = product_name.replace('(PRODUCT)', '')
            product_name = product_name.replace('RUS', '')
            product_name = product_name.replace('USA', '')
            product_name = product_name.replace('Apple', '')
            product_name = product_name.strip()
        except:
            pass
        price = product.find('div', {'class': "price_container"})
        price = str(price.find('p', {'class': "new_price"}).get_text())
        price = int(price.replace(' ', '')[:-1])
        old_price = str(price) + ' ₽.'
        price = int(price - price * 0.10)
        price = str(price) + ' ₽.'
        info = requests.get(product_link, params=par)
        product_soup = BeautifulSoup(info.text, 'html.parser')
        full_descritpion = ""
        descriptions = product_soup.find('div', {'class': 'characteristics_information'})
        descriptions = descriptions.findAll('div', {'class': 'item'})
        for i in range(0, len(descriptions)):
            try:
                key = str(descriptions[i].find('div', {'class': 'property'}).get_text()).strip()
                value = str(descriptions[i].find('div', {'class': 'description'}).get_text()).strip()
                all_list[key] = value
                if key in characteristics.keys():
                    characteristics[key] = value
                    # print(key.strip(), ":", value.strip())
                full_descritpion = full_descritpion + key.strip() + ": " + value.strip() + '\n'
            except:
                '''
                meta_key = descriptions[i].find('p').get_text()
                full_descritpion += str(meta_key).strip()
                full_descritpion += '\n'
                '''
                pass
        images_links = product_soup.find('div', {'class': 'product_top_container'})
        images_links = images_links.find('div', {'class': 'gallery_product'})
        images_links = (images_links.find('div', {'style': 'position:relative;'}))
        img_links = (images_links.find_all('a'))
        jpg_links = ""
        for elem in img_links:
            elem = str(elem)
            start = int(str(elem).find('srcset')) + 8
            end = str(elem).find('2x"') - 1
            srcset = elem[start:end].replace(' ', '%20')
            if srcset.startswith('https'):
                jpg_links = jpg_links + srcset + ', '
        '''
        try:
            vitrine = jpg_links[jpg_links.index("\n"):].replace('max-700', 'max-228')
        except:
            pass
        start = int(str(images_links).find('href')) + 6
        end = str(images_links).find('style="display') - 2
        for k in range(1, 5):
            product_images = product_images + "\n" + (
                product_image.replace(product_image[-7:-4], str(int(product_image[-7:-4]) + k)))'''
        small_descriptions = "Все решения, предпринятые на этапе разработки iPhone, направлены на повышение" \
                             " эффективности и удобства для пользователей. Тщательное создание концепции и" \
                             " последовательная реализация помогают производить технику, которой нет равных в своём" \
                             " сегменте. Именно этот модель определяет вектор развития индустрии и демонстрирует новые" \
                             " возможности и превосходства над конкурентами"
        cursor.execute(
            '''INSERT INTO "Edited" (id, Товар, Категория, Бренд, Вариант, Цена, "Старая цена", Склад, Артикул, 
                Видим, Рекомендуемый, Аннотация, Адрес, Описание, Изображения, "Заголовок страницы", "Ключевые слова", 
                "Версия ОС", "Емкость аккумулятора", "Количество SIM-карт", "Размеры (ШxВxТ)", "Тип SIM-карты",
                Управление, Процессор, "Размер изображения", Диагональ, "Диафрагмы основных (тыловых) камер", 
                "Макс. разрешение видео", "Разрешения основных (тыловых) камер", "Функция беспроводной зарядки", Аудио,
                 Вес, Датчики) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
            (None, product_name, "Смартфоны", "Apple", "", price, old_price, "7", "", 1, 0, '', '', small_descriptions,
             jpg_links[:-2], product_name, '', characteristics["Версия ОС на начало продаж"],
             characteristics["Емкость аккумулятора"],
             characteristics["Количество SIM-карт"], characteristics["Размеры (ШxВxТ)"],
             characteristics["Тип SIM-карты"], characteristics["Управление"], characteristics["Процессор"],
             characteristics["Размер изображения"], characteristics["Диагональ"],
             characteristics["Диафрагмы основных (тыловых) камер"], characteristics["Макс. разрешение видео"],
             characteristics["Разрешения основных (тыловых) камер"], characteristics["Функция беспроводной зарядки"],
             characteristics["Аудио"], characteristics["Вес"], characteristics["Датчики"]))
        sqliteConnection.commit()
        print(product_name, "||", price)
