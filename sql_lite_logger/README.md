#GoTouch Amalok: Monitoreo por GPS de unidades Autobuseras del Tecnológico de Costa Rica 
##  ¿Qué encontrará en esta carpeta?
Encontrará dos archivos ecritos en el lenguaje de Python, en los cuales se definirá un objecto de software que realizará lectura y escritura de datos estructurados mediante diccionarios para su respectivo respaldo. Además encontrará una serie de pruebas del uso de este módulo de respaldo de datos.

### Archivo de prueba test.py
Este archivo hace una instanciación de una clase de tipo  SQL_Lite_Logger, escribirá una serie de datos y hará luego una lectura a dos tablas predefinidas: una tabla alamacena los datos con clave de éxito y otros con clave de fallo.
Finalmente se hará un borrado de los datos en ambas tablas.
Los datos a escribir serán diccionarios de python con los sigueintes datos:
		
```python
{ 'date': 'datasamp'
	'latitude': 'double number'
	'longitue': 'double number'
	'altitude': 'double number'
	'speed'   : 'double number'    
	'status': 1:success during mqtt export or 2:fault sending the logs  }
```
### Archivo respaldo de datos SQL_Lite_Logger.py
Este archivo utiliza la biblioteca de python sqlite3 para poder definir un objeto que tenga las funcionalidades de respaldo de los datos.
Mediante la creación de dos tablas para almacenar los datos exitosamente enviados al servidor de mqtt y otra tabla para almacenar aquellos que no pudieron ser enviados para su posterior reintento de envío.
Esta clase tiene definido, además, funcones de lectura, escritura y borrado de datos para ambas tablas.
### Archivo utils.py
Este archivo sólo carga herramientas generales como creación de una marca de tiempo para el respaldo oportuno de los datos.
##  Flujo de Trabajo
El archivo test.py instancia al objecto SQL_lite_logger y realiza pruebas a los métodos
de lectrura, escritura y borrado de datos.
##  Referencias

### SQL Lite en python 
[Documentación oficial](https://docs.python.org/2/library/sqlite3.html)
