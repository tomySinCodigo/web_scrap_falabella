import pandas as pd
from bs4 import BeautifulSoup, ResultSet
from playwright.sync_api import sync_playwright
from pprint import pprint


def extraer_html(url:str):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        contenido = page.content()
        browser.close()
        return contenido
    
def obten_productos(url:str) -> ResultSet:
    html = extraer_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    # productos = soup.find_all(class_="grid-pod")
    productos = soup.find_all(class_="grid-pod")

    data = []
    for x, producto in enumerate(productos[:4]):
        print('PRODUCTO NUM:: ', x+1)
        # precio = producto.find('ol', class_='pod-prices').text
        data_precio = producto.find('ol', class_='pod-prices')
        con_desc = data_precio.find('span', class_='jsx-3451706699')
        if con_desc:
            con_desc = con_desc.text
        aux_precio = data_precio.find('li', class_='jsx-2128016101 prices-0')
        precio = aux_precio.find('span')
        if precio:
            precio = precio.text
        desc = data_precio.find('span', class_='discount-badge-item')
        if desc:
            desc = desc.text
        sin_desc = data_precio.find('li', class_='jsx-2128016101 prices-1')
        if sin_desc:
            sin_desc = sin_desc.text

        detalles = producto.find(class_='pod-details')
        # print(detalles)
        # vendedor = detalles.find('b', class_='pod-sellerText seller-text-rebrand')
        vendedor = detalles.find('b', class_='pod-sellerText')
        if vendedor:
            vendedor = vendedor.text

        marca = producto.find('b',class_='pod-title').text
        subtitulo = producto.find('b', class_='pod-subTitle').text
        badge = producto.find('span', class_='pod-badges-item')
        if badge:
            badge = badge.text
        imagen = producto.find('img')
    
        # print("::PROD:: ", producto.prettify())
        # head = producto.find('pod-head')
        # print(head)
        if imagen:
            imagen = imagen['src']

        calificacion = 0
        n_calificaciones = None
        try:
            estrellas = producto.find_all('i', class_='csicon-star_full_filled')
            estrellas_mitad = producto.find_all('i', class_='csicon-star_half_filled')
            calificacion += len(estrellas)
            calificacion += len(estrellas_mitad) * 0.5
        except Exception as err:
            print('error:: ', err)
        try:
            n_calificaciones = producto.find('span', class_='reviewCount')
            if n_calificaciones:
                n_calificaciones = n_calificaciones.text
        except Exception as err:
            print('ERR:: ', err)

        data.append({
            'subtitulo':subtitulo,
            'badge':badge,
            'marca':marca,
            'precio':precio,
            'calificacion':calificacion,
            'n_calificacion':n_calificaciones,
            'con_desc':con_desc,
            'desc':desc,
            'sin_desc':sin_desc,
            'vendedor':vendedor,
            'imagen':imagen,
        })
    return data

website = "https://www.falabella.com.pe/falabella-pe/collection/ver-todo-zapatos?sid=HO_CD_F18_GC_CAL_2770&page=2"
# pprint(obten_productos(website))

def escribe_csv():
    dc = obten_productos(website)
    df = pd.DataFrame.from_dict(dc)
    df.to_csv('falabella_1.csv')

# escribe_csv()