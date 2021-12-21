import argparse
import hashlib
import logging
from urllib.parse import urlparse
import pandas as pd
import nltk
from nltk.corpus import stopwords
# LAS LINEAS DE DEBAJO SE DEBEN EJECUTAR LA PRIMERA VEZ QUE SE EJECUTE EL CODIGO
# UNA VEZ EJECUTADAS, SE DUEDEN COMENTAR
# nltk.download('punkt')
# nltk.download('stopwords')

import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(archivo):
    logger.info('Empezando el proceso de Limpieza del Archivo')

    df = _read_data(archivo)
    newspaper_uid = _extract_newspaper_uid(archivo)
    df = _add_newspaper_uid_column(df, newspaper_uid)
    df = _extract_host(df)
    df = _fill_missing_titles(df)
    df = _generate_uids_for_rows(df)
    df = _remove_new_lines_from_body(df)
    df = _tokenize_column(df, 'title')
    df = _tokenize_column(df, 'body')
    df = _remove_duplicate_entries(df, 'title')
    df = _drops_rows_with_missing_values(df)
    _save_data(df, filename=archivo)

    return df



##Funciones que hacen la transformacion automatizada
def _read_data(filename):
    logger.info(f'Leyendo el archivo {filename}')
    return pd.read_csv(filename)


def _extract_newspaper_uid(filename):
    logger.info('Extrayendo el Newspaper_UID del archivo')
    newspaper_uid = filename.split('_')[0]

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


def _generate_uids_for_rows(df):
    logger.info('Generando uids para cada fila')

    uids = (
        df
        .apply( lambda row: hashlib.md5(bytes(row['url'].encode())) ,axis = 1 )
        .apply( lambda hash_object: hash_object.hexdigest() )
    )
    df['uid'] = uids

    return df.set_index('uid')


def _remove_new_lines_from_body(df):
    logger.info('Remover lineas de salto del body')
    stripped_body = (
        df
        .apply( lambda row: row['body'], axis=1 )
        .apply( lambda body: list(body) )
        .apply( lambda letters: list(map(lambda letter: letter.replace('\n', ' '), letters)) )
        .apply( lambda letters_list: ''.join(letters_list) )
    )

    df['body'] = stripped_body
    return df


def _tokenize_column(df, column_name):
    logger.info(f'Calculando la cantidad de tokens únicos en {column_name}')
    stop_words = set(stopwords.words('spanish'))

    n_tokens =  (
        df
        .dropna()
        .apply(lambda row: nltk.word_tokenize(row[column_name]), axis=1)
        .apply(lambda tokens: list(filter(lambda token: token.isalpha(), tokens)))
        .apply(lambda tokens: list(map(lambda token: token.lower(), tokens)))
        .apply(lambda word_list: list(filter(lambda word: word not in stop_words, word_list)))
        .apply(lambda valid_word_list: len(valid_word_list))
    )

    df['n_tokens_' + column_name] = n_tokens

    return df


def _remove_duplicate_entries(df, column_name):
    logger.info('Removiendo las entradas duplicadas')
    df.drop_duplicates(
        subset = [column_name],
        keep = 'first',
        inplace = True
    )

    return df


def _drops_rows_with_missing_values(df):
    logger.info('Eliminando las filas donde no hay valores')
    return df.dropna()


def _save_data(df, filename):
    logger.info(f'Guardando la informacin en _{filename}')
    df.to_csv(f'clean_{filename}')


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'archivo',
        help="Archivo con la informacion sucia",
        type=str
    )

    arg = parser.parse_args()

    df = main(arg.archivo)
    print(df)