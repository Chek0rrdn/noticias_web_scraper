import argparse
import logging
from urllib.parse import urlparse
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(archivo):
    logger.info('Empezando el proceso de Limpieza del Archivo')

    df = _read_data(archivo)
    newspaper_uid = _extract_newspaper_uid(archivo)
    df = _add_newspaper_uid_column(df, newspaper_uid)
    df = _extract_host(df)
    df = _fill_missing_titles(df)

    return df


##Funciones que hacen la transformacion automatizada
def _read_data(archivo):
    logger.info(f'Leyendo el archivo {archivo}')
    return pd.read_csv(archivo)


def _extract_newspaper_uid(archivo):
    logger.info('Extrayendo el Newspaper_UID del archivo')
    newspaper_uid = archivo.split('_')[0]

    logger.info(f'Newspaper_uid identificado: {newspaper_uid}')
    return newspaper_uid


def _add_newspaper_uid_column(df, newspaper_uid):
    logger.info(f'Llenando la columna Newspapaer_Uid con {newspaper_uid}')

    df['newspaper_uid'] = newspaper_uid
    return df


def _extract_host(df):
    logger.info('Extrayebdo el host de las URLs')
    df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)

    return df


def _fill_missing_titles(df):
    logger.info('Rellenando los titulosfaltantes')

    missing_titles_mask = df['title'].isna()

    missing_titles = (
        df[missing_titles_mask]['url'].str
        .extract(r'(?P<missing_titles>[^/]+$)')
        .applymap( lambda title: title.split('-') )
        .applymap( lambda title_word_list: ' '.join(title_word_list) )
    )

    df.loc[missing_titles_mask, 'title'] = missing_titles.loc[:, 'missing_titles']

    return df



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'archivo',
        help="Ruta a el archivo con informacion sucia",
        type=str
    )

    arg = parser.parse_args()

    df = main(arg.archivo)
    print(df)