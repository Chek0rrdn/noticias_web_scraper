import argparse
import logging

from common import config
logging.basicConfig(level=logging.INFO)


logger = logging.getLogger(__name__)


def _new_scraper(news_sites_uid):
    host = config()['news_sites'][news_sites_uid]['url']

    logging.info(f'Empezando el scrapping para {host}')


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