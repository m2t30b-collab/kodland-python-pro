"""Extraer noticias de la fuente indicada en el curso y resumir diez."""
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import pandas as pd
from resumidor import resumen_publicable

SOURCE = 'https://www.xataka.com/tag/ciencia-y-tecnologia'

def scrape_index(url=SOURCE):
    response = requests.get(url, timeout=25)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = []
    for a in soup.select('h2 a[href]'):
        link = a['href']
        if urlparse(link).hostname == 'www.xataka.com' and link not in urls:
            urls.append(link)
    return urls

def scrape_article(item):
    number, url = item
    response = requests.get(url, timeout=25)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    body = soup.select_one('.article-content') or soup.select_one('article')
    if body is None:
        raise ValueError('La página no contiene un artículo reconocible')
    text = ' '.join(p.get_text(' ', strip=True) for p in body.select('p'))
    if len(text) < 100:
        raise ValueError('No se pudo extraer suficiente texto')
    time = soup.select_one('time[datetime]')
    return {'noticia': number, 'url': url,
            'fecha': time.get('datetime', '') if time else '',
            'resumen': resumen_publicable(text, 25),
            'palabras_originales': len(text.split())}

def collect_news(n=10):
    urls = scrape_index()[:n]
    if len(urls) < n:
        raise ValueError(f'Solo se encontraron {len(urls)} enlaces, se necesitan {n}')
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(scrape_article, enumerate(urls, 1)))
    df = pd.DataFrame(rows)
    df.to_csv('noticias_resumidas.csv', index=False)
    return df

if __name__ == '__main__':
    print(collect_news().to_string(index=False))
