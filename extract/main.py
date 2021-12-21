import argparse
import csv
import datetime
import logging
import re
import os

from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

from news_page_object import *
from common import *

logging.basicConfig(level=logging.INFO)


logger = logging.getLogger(__name__)
link_bien_formado = re.compile(r'^https?://.+/+$')
es_ruta_raiz = re.compile(r'^/.+$')


@tiempo_de_ejecucion
def _new_scraper(news_sites_uid):
    host = config()['news_sites'][news_sites_uid]['url']

    logging.info(f'Empezando el scrapping para {host}')
    homepage = HomePage(news_sites_uid, host)

    articulos = []
    for link in homepage.article_links:
        # print(link)
        articulo = _fetch_article(news_sites_uid, host, link)

        if articulo:
            logger.info('Articulo recuperado!!!\n')
            articulos.append(articulo)
    
    _save_articles(news_sites_uid, articulos)


def _save_articles(news_sites_uid, articles):
    now = datetime.datetime.now().strftime('%d_%m_%Y')
    archivo_salida = f'{news_sites_uid}_{now}_articulos.csv'
    cabeceras_csv = list(filter(lambda property: not property.startswith('_'), dir(articles[0])))

    with open(f'{archivo_salida}', mode='w+') as f:
        writer = csv.writer(f)
        writer.writerow(cabeceras_csv)

        for article in articles:
            row = [ str(getattr(article, prop)) for prop in cabeceras_csv]
            writer.writerow(row)


def _build_link(host, link):
    if link_bien_formado.match(link):
        return link
    elif es_ruta_raiz.match(link):
        return f'{host}{link}'
    else:
        return f'{host}/{link}'


def _fetch_article(news_sites_uid, host, link):
    logger.info(f'Empezamos a recuperar los enlaces validos en {link}')

    articulo = None

    try:
        articulo = ArticlePage(news_sites_uid, _build_link(host, link))

    except(HTTPError, MaxRetryError) as e:
        logger.warning('Error mientras recuperamos el articulo\n', exc_info=False)

    if articulo and not articulo.body:
        logger.warning('Articulo invalido, no hay cuerpo en el articulo\n')
        return None
    
    return articulo



if __name__ == '__main__':
    parser = argparse.ArgumentParser()


    opciones_de_sitio = list(config()['news_sites'].keys())
    parser.add_argument(
        'news_sites',
        help = 'El sitio de noticias que quieres investigar',
        type = str,
        choices = opciones_de_sitio
    )

    args = parser.parse_args()
    _new_scraper(args.news_sites)