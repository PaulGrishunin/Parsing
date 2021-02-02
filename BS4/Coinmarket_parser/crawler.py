import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from multiprocessing import Pool
from colorama import init

def get_html(url):
    r = requests.get(url)
    return r.text


def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')

    tds = soup.find_all('td', class_="cmc-table__cell cmc-table__cell--sticky cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--sort-by__name")

    links = []

    for td in tds:
        a = td.find('a', class_="cmc-link").get('href')
        link = 'https://coinmarketcap.com' + a
        links.append(link)

    return links


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        name = soup.find('span', class_="sc-1eb5slv-0 sc-1308828-0 deLPiG").text.strip()
    except:
        name = ''
    try:
        price = soup.find('div', class_="priceValue___11gHJ").text.strip()
    except:
        price = ''
    data = {'name': name,
            'price': price}
    return data


def write_csv(data):
    with open('coinmarketcap.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow( (data['name'],
                          data['price']) )
        if data['name']:
            print('\033[93m', data['name'],'\033[00m', '-- \033[32m', data['price'],'\033[00m')


def make_all(url):
    html = get_html(url)
    data = get_page_data(html)
    write_csv(data)


def main():
    start = datetime.now()
    url = 'https://coinmarketcap.com/all/views/all/'

    all_links = get_all_links(get_html(url))

#With 1 thread
    for url in all_links:
       html = get_html(url)
       data = get_page_data(html)
       write_csv(data)
    end1 = datetime.now()

#Multiprocessing
    with Pool(8) as p:
        p.map(make_all, all_links)

    end2 = datetime.now()
    total1 = end1 - start
    total2 = end2 - end1
    print("1 Thread:", str(total1))
    print("Multiprocesses:", str(total2))
if __name__ == '__main__':
    main()
