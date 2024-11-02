# webscrapping
producto zapatos: del sitio falabella

## borrador.py
caracteristicas:

- [x] leer excel
- [x] extraer urls
- [x] obtener html de la pagina
- [ ] extraer info de los productos, todos los links del archivo excel (varias urls)
    - [x] obtener info de un producto
    - [x] obtener info de los productos en una pagina
        - [x] marca
        - [x] pendiente
        - [x] subtitulo
        - [x] vendedor
        - [x] precio con descuento
        - [x] precio sin descuento
        - [x] descuento
        - [x] calificacion
        - [ ] imagen
- [ ] guardar informacion
- [ ] realizar graficas con los datos obtenidos (seaborn)


Para obtener la info de cada producto:

## pruebas_scrap.py
Estoy haciendo pruebas por separado, con un solo producto para obtener toda la informacion
* para agilizar y facilitarme las pruebas con las funciones anteriores (las que tiene check) guarde el html de un solo producto en un archivo

## Manejo de errores
- he creado un modulo con clases para los errores de cada funcion
- acorte el codigo para cada clase
- ahora para crear otros errores es necesario solo heredar de la clase `MiError` y colocar la documentacion de la clase (esto se mostrara junto al error) tambien a la nueva clase de error se puede ir agregando mas strings de ser necesario

## en progreso
- para obtener imagen aun sigo haciendo pruebas (aun no las obtiene)