import pandas as pd
from pandas import DataFrame, Series
from bs4 import BeautifulSoup, ResultSet, Tag
from playwright.sync_api import sync_playwright
from returns.io import IOResult, IOSuccess, IOFailure
from returns.pipeline import is_successful
from errores import (
    MiError, ErrorExcel, ErrorExtractUrls, ErrorPlaywright,
    ErrorBs4Parser, ErrorBs4Find, ErrorBs4SelOne,
    ErrorGetInfo, ErrorGetPLP, ErrorGetProductosInfo,
    ErrorCalification, ErrorGetImagen
)


def read_excel(excel_file: str) -> IOResult[DataFrame, ErrorExcel]:
    try:
        return IOSuccess(pd.read_excel(excel_file, header=None))
    except Exception as err:
        return IOFailure(ErrorExcel(err))

def extract_urls(df: DataFrame) -> IOResult[Series, ErrorExtractUrls]:
    try:
        return IOSuccess(df[0])
    except Exception as err:
        return IOFailure(ErrorExtractUrls(err))

def get_html_content(url: str) -> IOResult[str, ErrorPlaywright]:
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            # browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            page.wait_for_url(url)
            content = page.content()
            browser.close()
            return IOSuccess(content)
    except Exception as err:
        return IOFailure(ErrorPlaywright(err))

def soup_bs4(
    html: str, features: str = "html.parser"
) -> IOResult[BeautifulSoup, ErrorBs4Parser]:
    try:
        return IOSuccess(BeautifulSoup(html, features))
    except Exception as err:
        return IOFailure(ErrorBs4Parser(err, f'features:{features}'))

def find(soup:BeautifulSoup, tag:Tag="div", attrs:str="grid-pod", all:bool=False) -> IOResult[ResultSet, ErrorBs4Find]:
    try:
        return IOSuccess(soup.find_all(tag, attrs) if all else soup.find(tag, attrs))
    except Exception as err:
        return IOFailure(ErrorBs4Find(err, f"{tag}:{attrs}"))

def text(resultset: ResultSet) -> str:
    return resultset.text if resultset else ""

def select_one(soup:BeautifulSoup, selector:str) -> IOResult[ResultSet, ErrorBs4SelOne]:
    try:
        return IOSuccess(text(soup.select_one(selector)))
    except Exception as err:
        return IOFailure(ErrorBs4SelOne(err, f"selector:{selector}"))
    
def get_calification(resulset:ResultSet) -> IOResult[float, ErrorCalification]:
    try:
        return IOSuccess(
            len(get(find(resulset, tag='i', attrs='csicon-star_full_filled', all=True))) + \
            len(get(find(resulset, tag='i', attrs='csicon-star_half_filled', all=True)))*0.5
        )
    except Exception as err:
        return IOFailure(ErrorCalification(err))
    
def get_image(resulset:ResultSet) -> IOResult[str, ErrorGetImagen]:
    try:
        pic = get(select_one(resulset, 'picture.jsx-1996933093 source.jsx-1996933093'))
        print(pic, len(pic), type(pic))
        if pic:
            # src = get(pic, tag='source', attrs='jsx-1996933093')
            # src = get(pic, tag='img', attrs='jsx-1996933093')
            src = get(pic)
            print("SOURCE::: ", src['srcset'])
            image = src['srcset'].split(',')[0].strip() if pic and src else ''
            # .bind(lambda x: x['srcset'].split(',')[0].strip() if x else '')
        return IOSuccess(image)
    except Exception as err:
        return IOFailure(ErrorGetImagen(err))

def get_info_product(soup:BeautifulSoup) -> IOResult[dict, ErrorGetInfo]:
    try:
        return IOSuccess(
            {
                'marca':get(select_one(soup, 'div.pod-details b.pod-title')),
                'pendiente':get(select_one(soup, 'div.pod-details span.pod-badges-item')),
                'subtitulo':get(select_one(soup, 'div.pod-details b.pod-subTitle')),
                'vendedor':get(select_one(soup, 'div.pod-details b.pod-sellerText')),
                'precio con descuento':get(select_one(soup, 'div.pod-summary span.line-height-22')).split('/')[-1].strip(),
                'precio sin descuento':get(select_one(soup, 'div.pod-summary li.jsx-2128016101.prices-1')).split('/')[-1].strip(),
                'descuento':get(select_one(soup, 'div.pod-summary span.discount-badge-item')),
                'calificacion':get(get_calification(soup)),
                # 'img':get(get_image(soup))
            }
        )
    except Exception as err:
        return IOFailure(ErrorGetInfo(err))

def get(result: IOResult):
    return result.bind(lambda r:r) if is_successful(result) else result.failure()



# TESTS
def get_link(df: DataFrame) -> IOResult[Series, MiError]:
    """obten un link del archivo excel"""
    try:
        return IOSuccess(df[0][1])
    except Exception as error:
        return IOFailure(MiError(error, get_link.__name__))

def get_productos_html() -> IOResult:
    """obten lista productos [html] de una pagina"""
    return (
        read_excel("DataLinks/Libro.xlsx")
        .bind(get_link)
        .bind(get_html_content)
        .bind(lambda html: soup_bs4(html))
        .bind(lambda prods:find(prods, all=True))
    )

def get_productos_info():
    """obten info de todos los productos de una pagina"""
    try:
        return IOSuccess(map(get_info_product, get(get_productos_html())))
    except Exception as err:
        return IOFailure(ErrorGetProductosInfo(err))

def main() -> None:
    # obteniendo los productos de una pagina (~ 48 productos)
    prods = get(get_productos_info())
    # print(type(prods))
    for p in list(prods)[0:12]:
        print(p)

main()
