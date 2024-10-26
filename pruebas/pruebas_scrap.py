import pandas as pd
from pandas import DataFrame, Series
from bs4 import BeautifulSoup, ResultSet, Tag
from playwright.sync_api import sync_playwright
from returns.io import IOResult, IOSuccess, IOFailure
from returns.pipeline import is_successful


def get(soup:BeautifulSoup, tag:Tag='div', attrs:str='grid-pod', all:bool=False) -> IOResult[ResultSet, str]:
    try:
        return IOSuccess(soup.find_all(tag, attrs) if all else soup.find(tag, attrs))
    except Exception as err:
        return IOFailure(f"{get.__name__} {tag}:{attrs} ::-> {err}")
    
def get_value(result:IOResult):
    return result

def respuesta(res:IOResult):
    return res.bind(get_value) if is_successful(res) else res.failure()
    
def text(resultset:ResultSet) -> str | None:
    return resultset.text if resultset else ""

def select_one(soup:BeautifulSoup, selector:str) -> IOResult[ResultSet, str]:
    try:
        return IOSuccess(soup.select_one(selector))
    except Exception as err:
        return IOFailure(f"{select_one.__name__} selector:{selector} ::-> {err}")
    
def obtenCalificacion(resulset:ResultSet) -> IOResult[float, str]:
    calificacion = 0
    try:
        calificacion += len(respuesta(get(resulset, tag='i', attrs='csicon-star_full_filled', all=True)))
        calificacion += len(respuesta(get(resulset, tag='i', attrs='csicon-star_half_filled', all=True)))*0.5
        return IOSuccess(calificacion)
    except Exception as err:
        return IOFailure(f'Calificacion:: {calificacion}, {err}')

def obtenImagen(resulset:ResultSet) -> IOResult[str, str]:
    try:
        pic = respuesta(get(resulset, tag='picture', attrs='jsx-1996933093'))
        print("picc:  ", pic)
        if pic:
            # src = get(pic, tag='source', attrs='jsx-1996933093')
            src = respuesta(get(pic, tag='img', attrs='jsx-1996933093'))
            # print('src::', src)
            print(src)
            print(f'TIPO: {type(src)}')
            image = src['srcset'].split()[0].strip() if pic and src else ''
            print(':::::::::::: IMAGE:::: ', image)
        return IOSuccess(image)
    except Exception as err:
        return IOFailure(f"obtenIMG - pic:{pic}, {err}")


def get_info(soup:BeautifulSoup, tag:Tag='div', attrs:str='grid-pod'):
    try:
        return IOSuccess(
            {
                'marca':text(respuesta(select_one(soup, 'div.pod-details b.pod-title'))),
                'badge':text(respuesta(select_one(soup, 'div.pod-details span.pod-badges-item'))),
                'subtitulo':text(respuesta(select_one(soup, 'div.pod-details b.pod-subTitle'))),
                'vendedor':text(respuesta(select_one(soup, 'div.pod-details b.pod-sellerText'))),
                'precio con descuento':text(
                    respuesta(select_one(soup, 'div.pod-summary span.line-height-22'))
                ).split('/')[-1].strip(),
                'descuento':text(respuesta(select_one(soup, 'div.pod-summary span.discount-badge-item'))),
                'precio sin descuento':text(
                    respuesta(select_one(soup, 'div.pod-summary li.jsx-2128016101 prices-1'))
                ).split('/')[-1].strip(),
                'calificacion':respuesta(obtenCalificacion(soup)),
                'imagen':respuesta(obtenImagen(soup))
            }
        )
    except Exception as err:
        return IOFailure(f'falla [get_info]:: {err}')
    


# TEST 
# TEST 
# from pathlib import Path
# print("\n", Path().cwd())
archivo = 'pruebas/elemento.html'

def simula_scrap_elemento() -> str:
    with open(archivo) as f:
        return f.read()


html_str = simula_scrap_elemento()
# Crear un objeto Beautiful Soup
soup = BeautifulSoup(html_str, 'html.parser')
# Acceder al primer tag <div>
html = soup.find('div')
# print('TIPO:: ', type(html))
# obteniendo info del producto
# res = get_info(html)
res = respuesta(get_info(html))
# print("\n", res, type(res), "\n")
from pprint import pprint
print()
pprint(res)
print()
# TEST 
# TEST 