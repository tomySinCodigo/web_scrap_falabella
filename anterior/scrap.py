import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def extraer_html(url:str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        contenido = page.content()
        browser.close()
        return contenido
    
def obten_info():
    website = "https://www.falabella.com.pe/falabella-pe/collection/ver-todo-zapatos?sid=HO_CD_F18_GC_CAL_2770&page=2"
    html = extraer_html(website)
    soup = BeautifulSoup(html, 'html.parser')
    elementos = soup.find_all(class_="grid-pod")

    uno = elementos[0]
    precio = uno.find('ol', class_='pod-prices').text
    marca = uno.find('b',class_='pod-title').text
    subtitulo = uno.find('b', class_='pod-subTitle').text
    badge = uno.find('span', class_='pod-badges-item').text
    imagen = uno.find('img')['src']
    
    print(f"precio: ", precio)
    print(f"titulo: ", marca)
    print(f"subtitulo: {subtitulo}")
    print(f"badge: {badge}")
    print(f"imagen: {imagen}")

    calificacion = 0
    try:
        estrellas = uno.find_all('i', class_='csicon-star_full_filled')
        estrellas_mitad = uno.find_all('i', class_='csicon-star_half_filled')
        calificacion += len(estrellas)
        calificacion += len(estrellas_mitad) * 0.5
    except Exception as err:
        print('error:: ', err)
    print(f"calificaion: {calificacion}")
    try:
        n_calificaciones = uno.find('span', class_='reviewCount').text
        print(f"reviews:: {n_calificaciones}")
    except Exception as err:
        print('ERR:: ', err)

obten_info()