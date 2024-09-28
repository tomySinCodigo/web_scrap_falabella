# Obtencion de informacion de un producto de Falabella

url del sitio que use

`https://www.falabella.com.pe/falabella-pe/collection/ver-todo-zapatos?sid=HO_CD_F18_GC_CAL_2770&page=2`

# scrap_2.py
Este archivo captura la info de los productos de una sola pagina (**48** productos), el archivo es un borrador aun (esta muy desordenado) pero funciona

Guarda la info obtenida en un archivo **falabella_1.csv** 

Hay un problema al obtener las imagenes solo obtiene unas cuantas


**captura del producto**

![](md/muestra_scrap2.png)


**data obtenida:**

en esta muestra obtiene info de 4 productos

aun hay cosas que corregir:
 - borrar espacios en blanco con strip
 - quitar parentesis,
 - cambiar S por dolar o quitarlo
 - cambiar None por otro dato mas adecuado


```python
[{'badge': 'Llega mañana',
  'calificacion': 4.5,
  'con_desc': 'S/  139.30  ',
  'desc': '-30%',
  'imagen': 'https://www.falabella.com.pe/cdn-cgi/imagedelivery/4fYuQyy-r8_rpBpcY7lH_A/falabellaPE/19852120_1/width=240,height=240,quality=70,format=webp,fit=pad',
  'marca': 'PUMA',
  'n_calificacion': '(8)',
  'precio': 'S/  139.30  ',
  'sin_desc': 'S/  199   ',
  'subtitulo': 'Zapatillas urbanas Mujer Smash 3.0 L Blanco',
  'vendedor': 'Por Falabella'},

 {'badge': 'Llega mañana',
  'calificacion': 4.5,
  'con_desc': 'S/  219  ',
  'desc': None,
  'imagen': 'https://www.falabella.com.pe/cdn-cgi/imagedelivery/4fYuQyy-r8_rpBpcY7lH_A/falabellaPE/20442661_1/width=240,height=240,quality=70,format=webp,fit=pad',
  'marca': 'ADIDAS',
  'n_calificacion': '(94)',
  'precio': 'S/  219  ',
  'sin_desc': None,
  'subtitulo': 'Zapatillas Urbanas Mujer Breaknet Sleek Azul',
  'vendedor': 'Por Falabella'},

 {'badge': 'Llega mañana',
  'calificacion': 4.5,
  'con_desc': 'S/  118.30  ',
  'desc': '-30%',
  'imagen': 'https://www.falabella.com.pe/cdn-cgi/imagedelivery/4fYuQyy-r8_rpBpcY7lH_A/falabellaPE/20492693_1/width=240,height=240,quality=70,format=webp,fit=pad',
  'marca': 'PUMA',
  'n_calificacion': '(31)',
  'precio': 'S/  118.30  ',
  'sin_desc': 'S/  169   ',
  'subtitulo': 'Zapatillas urbanas Mujer Bari Casual CV',
  'vendedor': 'Por Falabella'},

 {'badge': 'Llega mañana',
  'calificacion': 5.0,
  'con_desc': 'S/  137.40  ',
  'desc': '-40%',
  'imagen': 'https://www.falabella.com.pe/cdn-cgi/imagedelivery/4fYuQyy-r8_rpBpcY7lH_A/falabellaPE/20442923_1/width=240,height=240,quality=70,format=webp,fit=pad',
  'marca': 'ADIDAS',
  'n_calificacion': '(766)',
  'precio': 'S/  137.40  ',
  'sin_desc': 'S/  229   ',
  'subtitulo': 'Zapatillas Urbanas Mujer Courtblock',
  'vendedor': 'Por Falabella'}]
```
## Muestra del archivo CSV generado
![](md/scrap2_archivoCSV.png)



---

# scrap.py
**captura del producto**

![](md/prod_1.png)


**data obtenida:**

```python
precio:  S/  219
titulo:  ADIDAS
subtitulo: Zapatillas Urbanas Mujer Breaknet Sleek Azul
badge: Llega mañana
imagen: https://www.falabella.com.pe/cdn-cgi/imagedelivery/4fYuQyy-r8_rpBpcY7lH_A/falabellaPE/20442660_1/width=240,height=240,quality=70,format=webp,fit=pad
calificaion: 4.5
reviews:: (89)
```

imagen obtenida:

![](https://www.falabella.com.pe/cdn-cgi/imagedelivery/4fYuQyy-r8_rpBpcY7lH_A/falabellaPE/20442660_1/width=240,height=240,quality=70,format=webp,fit=pad)

