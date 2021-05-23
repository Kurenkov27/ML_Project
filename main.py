import csv
import os
import urllib.request
import requests
import bs4
from PIL import Image


def run_scrapper():

    pages = range(1, 2)

    for page in pages:
        url = f'https://auto.ria.com/uk/legkovie/?page={ page }'
        page = requests.get(url)

        soup = bs4.BeautifulSoup(page.text, 'html.parser')

        with open('csv_data_file.csv', 'a', encoding='UTF8') as f:
            header = ['name', 'price']
            writer = csv.writer(f)
            writer.writerow(header)

        for item in soup.select('.address'):
            name = item.text
            url_page = item.get('href')
            page_item = requests.get(url_page)
            soup_2 = bs4.BeautifulSoup(page_item.text, 'html.parser')
            img_url = soup_2.find_all('img', attrs={'class': 'outline m-auto'})[0].get('src')
            price = soup_2.find_all('div', attrs={'class': 'price_value'})[0].find('strong').getText()
            urllib.request.urlretrieve(img_url, 'images/' + os.path.basename(f'{name}.jpg'))
            with open('csv_data_file.csv', 'a', encoding='UTF8') as f:
                writer = csv.writer(f)
                data = [name, price]
                writer.writerow(data)


if __name__ == '__main__':
    run_scrapper()

