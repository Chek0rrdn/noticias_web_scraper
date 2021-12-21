import argparse
import logging

from sqlalchemy import engine
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import pandas as pd

from article import Article
from base import Base, engine, Session


def main(filename):
    Base.metadata.create_all(engine)
    session = Session()
    articles = pd.read_csv(filename)

    for index, row in articles.iterrows():
        logger.info(f"Cargando el uid del articulo del {row['uid']} dentro de la BD")
        article = Article(
            row['uid'],
            row['body'],
            row['host'],
            row['newspaper_uid'],
            row['n_tokens_body'],
            row['n_tokens_title'],
            row['title'],
            row['url']
        )
        session.add(article)
    
    session.commit()
    session.close()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'archivo',
        help="El archivo al que deseas cargar en la BD",
        type=str
    )

    args = parser.parse_args()

    main(args.archivo)
