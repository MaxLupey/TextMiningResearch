import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm

with open('result.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['text', 'target']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for i in tqdm(range(1, 795), desc='Pages', unit='page'):
        url = f'https://www.politifact.com/factchecks/?page={i}'

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        articles = soup.find_all('article', class_='m-statement')
        for article in tqdm(articles, desc='Processing articles', unit='article'):
            article_text = article.find('div', class_='m-statement__quote').find('a').text
            image_alt = article.find('div', class_='m-statement__content').find('img', class_='c-image__thumb')['alt']
            writer.writerow({'text': article_text, 'target': image_alt})

print('The data was successfully written to the result.csv file')
