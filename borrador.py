import pandas as pd
from pandas import DataFrame, Series
from bs4 import BeautifulSoup, ResultSet, Tag
from playwright.sync_api import sync_playwright
from returns.io import IOResult, IOSuccess, IOFailure
from returns.pipeline import is_successful


# esto estara en otro archivo
class MiError(Exception):
    def __init__(self, error, function_name):
        super().__init__(f"Error, {function_name}: {error}")
# esto estara en otro archivo


def read_excel(excel_file: str) -> IOResult[DataFrame, str]:
    try:
        return IOSuccess(pd.read_excel(excel_file, header=None))
    except Exception as err:
        return MiError(err, read_excel.__name__)

def extract_urls(df: DataFrame) -> IOResult[Series, MiError]:
    try:
        return IOSuccess(df[0])
    except Exception as err:
        return IOFailure(MiError(err, extract_urls.__name__))

def get_html_content(url: str) -> IOResult[str, MiError]:
    try:
        with sync_playwright() as p:
            # browser = p.chromium.launch(headless=False)
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            page.wait_for_url(url)
            content = page.content()
            browser.close()
            return IOSuccess(content)
    except Exception as err:
        return IOFailure(MiError(err, get_html_content.__name__))

def soup_bs4(
    html: str, features: str = "html.parser"
) -> IOResult[BeautifulSoup, MiError]:
    try:
        return IOSuccess(BeautifulSoup(html, features))
    except Exception as err:
        return IOFailure(MiError(err, soup_bs4.__name__))

def find(soup:BeautifulSoup, tag:Tag="div", attrs:str="grid-pod", all:bool=False) -> IOResult[ResultSet, MiError]:
    try:
        return IOSuccess(soup.find_all(tag, attrs) if all else soup.find(tag, attrs))
    except Exception as err:
        return IOFailure(MiError(err, f"{find.__name__} {tag}:{attrs}"))

def text(resultset: ResultSet) -> str:
    return resultset.text if resultset else ""

def select_one(soup:BeautifulSoup, selector:str) -> IOResult[ResultSet, str]:
    try:
        return IOSuccess(text(soup.select_one(selector)))
    except Exception as err:
        return IOFailure(f"{select_one.__name__} selector:{selector} ::-> {err}")

def get_info_product(soup:BeautifulSoup) -> IOResult[dict, MiError]:
    try:
        return IOSuccess(
            {
                'marca':get(select_one(soup, 'div.pod-details b.pod-title')),
                'pendiente':get(select_one(soup, 'div.pod-details span.pod-badges-item')),
                'subtitulo':get(select_one(soup, 'div.pod-details b.pod-subTitle')),
                'vendedor':get(select_one(soup, 'div.pod-details b.pod-sellerText')),
                'precio con descuento':get(select_one(soup, 'div.pod-summary span.line-height-22')).split('/')[-1].strip(),

            }
        )
    except Exception as err:
        return IOFailure(MiError(err, f"{get_info_product.__name__}"))

def get(result: IOResult):
    return result.bind(lambda r:r) if is_successful(result) else result.failure()



# TESTS
def get_link(df: DataFrame) -> IOResult[Series, MiError]:
    try:
        return IOSuccess(df[0][1])
    except Exception as error:
        return IOFailure(MiError(error, get_link.__name__))

def main() -> None:
    # obteniendo los productos de una pagina (~ 48 productos)
    elementos = get(
        read_excel("DataLinks/Libro.xlsx")
        .bind(get_link)
        .bind(get_html_content)
        .bind(lambda html: soup_bs4(html))
        .bind(lambda prods:find(prods, all=True))
    )
    # estp es solo para ir comprobando, que obtiene info correctamente
    print(f'TIPO: {type(elementos)}')
    elementos = map(get_info_product, elementos)
    for e in elementos:
        print(e)
    # obteniendo los productos de una pagina (~ 48 productos)


main()
