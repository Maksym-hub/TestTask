import requests
from bs4 import BeautifulSoup
import csv
import os

URL = 'https://www.yelp.com/search?find_desc=Vegan%20Cafe&find_loc=San%20Francisco%2C%20CA'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.344'}
HOST = 'https://www.yelp.com/'
FILE = 'rest.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_='  text__09f24__2tZKC text-color--black-extra-light__09f24__38DtK text-align--left__09f24__3Drs0 text-size--large__09f24__3-9KJ')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('li', class_=' border-color--default__09f24__R1nRO')

    rest = []
    for item in items:
        rest.append({
            'title': item.find('a', class_='link__09f24__1kwXV link-color--inherit__09f24__3PYlA link-size--inherit__09f24__2Uj95').find_next('target name').get_text(strip=True),
            'telephone': item.find('p', class_='text__09f24__2tZKC text-color--black-extra-light__09f24__38DtK text-align--right__09f24__1TIxB text-size--small__09f24__1Z_UI').get_text(),
            'site': HOST + item.find('a', class_='link__09f24__1kwXV link-color--inherit__09f24__3PYlA link-size--inherit__09f24__2Uj95').get('href'),
            'Tags': item.find('p', class_=' text__09f24__2tZKC text-color--black-extra-light__09f24__38DtK text-align--left__09f24__3Drs0').get_text(),
           # 'city': item.find('svg', class_='svg_i16_pin').find_next('span').get_text(),
        })
    return rest


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Телефон', 'Веб-сайт', 'Тэги'])
        for item in items:
            writer.writerow([item['title'], item['telephone'], item['site'], item['Tags']])


def parse():
    URL = input('Введите URL: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        rest = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            rest.extend(get_content(html.text))
        save_file(rest, FILE)
        print(f'Получено {len(rest)} ресторанов')
        os.startfile(FILE)
    else:
        print('Error')


parse()
