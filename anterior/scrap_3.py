import pandas as pd
from pandas import DataFrame, Series
from bs4 import BeautifulSoup, ResultSet, Tag
from playwright.sync_api import sync_playwright
from returns.io import IOResult, IOSuccess, IOFailure
import colorama
from pprint import pprint
from time import sleep


class MiError(Exception):
    def __init__(self, error, msg='mi error'):
        self.message = f"{msg}: {error}"
        super().__init__(f"ERROR: {self.message}")


def read_excel_py(excel_file: str) -> DataFrame:
    try:
        return pd.read_excel(excel_file, header=None)
    except Exception as err:
        raise MiError(err, "lectura excel")

def extrae_urls(df: DataFrame) -> Series:
    return df[0][1:]

def extraer_info(URL: str):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            # browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(URL)
            page.wait_for_url(URL)
            content = page.content()
            browser.close()
            return content
    except Exception as err:
        raise MiError(err, "playwright no pudo obtener informacion.")

def soup_bs4(html:str, features:str ="html.parser") -> BeautifulSoup:
    try:
        return BeautifulSoup(html, features)
    except Exception as err:
        raise MiError(err, "bs4 parser")

def get(soup:BeautifulSoup, tag:Tag='div', attrs:str='grid-pod', f_all:bool=False) -> ResultSet:
    try:
        return soup.find_all(tag, attrs) if f_all else soup.find(tag, attrs)
    except Exception as err:
        raise MiError(err, f"FIND {tag}:{attrs}")

def scrapper(soup:BeautifulSoup, tag:Tag='div', attrs:str='grid-pod', **kw) -> ResultSet[Tag]:
    try:
        dc = []
        productos = get(soup, tag, attrs, f_all=True)
        for i, producto in enumerate(productos):
            detalle = get(producto, attrs='pod-details')
            detalle2 = get(producto, attrs='pod-summary')
            dc.append(
                {
                    'num item':i+1,
                    'badge':text(get(producto, tag='span', attrs='pod-badges-item')),
                    'marca':text(get(detalle, tag='b', attrs='pod-title')),
                    'subtitulo':text(get(detalle, tag='b', attrs='pod-subTitle')),
                    'vendedor':text(get(detalle, tag='b', attrs='pod-sellerText')),
                    'precio con descuento':text(get(detalle2, tag='span', attrs='line-height-22')).split('/')[-1].strip(),
                    'descuento':text(get(detalle2, tag='span', attrs='discount-badge-item')),
                    'precio sin descuento':text(get(detalle2, tag='li', attrs='jsx-2128016101 prices-1')).split('/')[-1].strip(),
                    'calificacion':obtenCalificacion(detalle2),
                    'img':obtenImagen(producto)
                }
            )
        return dc
    except Exception as err:
        raise MiError(err, f'::SCRAPPER:: {len(dc)}')

def text(resultset:ResultSet) -> str | None:
    return resultset.text if resultset else ''

def obtenCalificacion(resulset:ResultSet) -> float:
    calificacion = 0
    try:
        calificacion += len(get(resulset, tag='i', attrs='csicon-star_full_filled', f_all=True))
        calificacion += len(get(resulset, tag='i', attrs='csicon-star_half_filled', f_all=True))*0.5
        return calificacion
    except Exception as err:
        raise MiError(err, f'Calificacion:: {calificacion}')

def obtenImagen(resulset:ResultSet) -> str:
    try:
        pic = get(resulset, tag='picture', attrs='jsx-1996933093')
        if pic:
            # src = get(pic, tag='source', attrs='jsx-1996933093')
            src = get(pic, tag='img', attrs='jsx-1996933093')
        return src['srcset'].split()[0].strip() if pic and src else ''
    except Exception as err:
        raise MiError(err, f"obtenIMG[pic]:{pic}")

def getProductosPage(url:str) ->list:
    return scrapper(soup_bs4(extraer_info(url)))

def getProductosPages(lista_urls:list) ->list:
    return [e for li in map(getProductosPage, lista_urls) for e in li]

def escribe_csv():
    archivo = "github/dw/Libro.xlsx"
    data = getProductosPages(extrae_urls(read_excel_py(archivo)))
    print("cantidad de productos:: ", len(data))
    pd.DataFrame(data).to_csv('productos_falabella_vp.csv')

def test():
    # print(len(elems), ' paginas', type(elems))

    # print("LINK 1:: ", pagina1)
    # obt = extraer_info(pagina1)
    # # print(obt)
    # sopa = soup_bs4(obt)
    # print("SOPA:: ", type(sopa))
    # li_scrap = scrapper(sopa)
    # print("RES::", len(li_scrap), type(li_scrap))
    # pprint(li_scrap)

    # li = getProductosPage(pagina1)
    # print(len(li), li[-1])
    # data = [e for li in map(getProductosPage, elems) for e in li]
    # print(len(data), type(data), data[-1])

    # test para obtner los productos de una sola pagina
    archivo = "github/dw/Libro.xlsx"
    elems = extrae_urls(read_excel_py(archivo))
    pagina1 = elems.iloc[0]
    prod = getProductosPage(pagina1)
    pprint(prod)

    # obten la info de todos los productos de los lonks del archivo excel
    # escribe_csv()


test()
