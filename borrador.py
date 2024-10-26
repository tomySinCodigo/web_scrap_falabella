import pandas as pd
from pandas import DataFrame, Series
from bs4 import BeautifulSoup, ResultSet, Tag
from playwright.sync_api import sync_playwright
from returns.io import IOResult, IOSuccess, IOFailure
from returns.pipeline import is_successful

# esto estara en otro archivo
class MiError(Exception):
    def __init__(self, error, function_name):
        super().__init__(f'Error, {function_name}: {error}')


def errorExcel(error: Exception) -> IOFailure[str]:
    if isinstance(error, FileNotFoundError):
        return IOFailure('ERROR: el archivo no fue encontrado.')
    elif isinstance(error, pd.errors.EmptyDataError):
        return IOFailure('ERROR: el archivo esta vacio.')
    elif isinstance(error, pd.errors.ParserError):
        return IOFailure('ERROR: no se pudo analizar el archivo.')
    else:
        return IOFailure(f'ERROR: inesperado: {error}')
# esto estara en otro archivo

def read_excel(excel_file:str) -> IOResult[DataFrame, str]:
    try:
        return IOSuccess(pd.read_excel(excel_file, header=None))
    except Exception as err:
        return errorExcel(err)
    
def extract_urls(df: DataFrame) -> IOResult[Series, MiError]:
    try:
        return IOSuccess(df[0])
    except Exception as err:
        return IOFailure(MiError(err, extract_urls.__name__))

def get_hmlt_content(url:str) -> IOResult[str, MiError]:
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url)
            page.wait_for_url(url)
            content = page.content()
            browser.close()
            return IOSuccess(content)
    except Exception as err:
        return IOFailure(MiError(err, get_hmlt_content.__name__))
    
def soup_bs4(html:str, features:str ="html.parser") -> IOResult[BeautifulSoup, MiError]:
    try:
        return IOSuccess(BeautifulSoup(html, features))
    except Exception as err:
        return IOFailure(MiError(err, soup_bs4.__name__))
    
def get(soup:BeautifulSoup, tag:Tag='div', attrs:str='grid-pod', f_all:bool=False) -> IOResult[ResultSet, MiError]:
    try:
        return IOSuccess(soup.find_all(tag, attrs) if f_all else soup.find(tag, attrs))
    except Exception as err:
        return IOFailure(MiError(err, f"{get.__name__} {tag}:{attrs}"))
    
def get_info_product(soup:BeautifulSoup, tag:Tag='div') -> IOResult[dict, MiError]:
    try:
        return IOSuccess(
            {
                'badge':text(
                    get(soup, attrs='pod-details').bind(
                    lambda x:get(x, tag='span', attrs='pod-badges-item')
                    ).bind(get_value)
                ),
                'marca':text(
                    get(soup, attrs='pod-summary').bind(
                        lambda t:get(t, tag='b', attrs='pod-title')
                    ).bind(get_value)
                )
            }
        )
    except Exception as err:
        return IOFailure(MiError(err, f"{get_info_product.__name__} tag:{tag}"))

def text(resultset:ResultSet) -> str | None:
    return resultset.text if resultset else ""

def get_productos_info():
    pass
    


# TESTS
from pathlib import Path


def respuesta(result:IOResult):
    if is_successful(result):
        return result.bind(get_value)
    else:
        return result.failure()

def get_value(result:IOResult):
    return result


# leer el archivo excel
archivo_excel = 'DataLinks/Libro.xlsx'
if Path(archivo_excel).exists():
    # res = respuesta(read_excel('archivo_noexiste.xlsx')) # error
    # res = respuesta(read_excel('SRC/DataLinks/Libro.xlsx'))
    # print(res, type(res))

    # obtener el html de la pagina
    link = respuesta(read_excel(archivo_excel))[0][1] # obtengo solo un link, para pruebas
    # print(link, type(link))
    html = respuesta(get_hmlt_content(link))
    # print(html, type(html))

    # obtener PLP
    scrap = respuesta(get(soup_bs4(html).bind(get_value), f_all=True))
    # print(scrap, type(scrap))
    # extraigo solo un producto, para realizar pruebas
    elemento = scrap[0]
    print(elemento, type(elemento))
    # info_prod = get_info_product(elemento)
    # print(info_prod, type(info_prod))

    # escribe elemento
    with open('pruebas/elemento.html', 'w') as f:
        f.write(str(elemento))
    print("elemento html creado")

else:
    print(
        'la ruta del archivo excel es erronea: ' \
        f'{Path(".").cwd() / Path(archivo_excel)}'
    )



