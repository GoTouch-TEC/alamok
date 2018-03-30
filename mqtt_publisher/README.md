#GoTouch Amalok: Monitoreo por GPS de unidades Autobuseras del Tecnológico de Costa Rica 
##  ¿Qué encontrará en esta carpeta?
Esta carpeta contiene la definición de una Class(POO), desarrollada en Python, que se comunica con un servidor MQTT y un archivo de pruebas que hace la prueba de concepto del caso.
Acontinuación se detallarán los pormenores de cada uno de los dos archivos involucrados.
### Archivo de prueba test.py
Este archivo hace una instaciación de la clase de tipo Publisher, definida en el archivo publisher.py. Debido a que la clase Publisher hereda de un objeto de tipo threading.Thread, este debe de ser iniciado y controlado mediante el hilo principal  en caso de que se interrumpa la aplicación.
### Archivo Clase de módulo de comunicación MQTT
Esta es la definicón de la clase Publisher, dicha clase hereda de threading.Thread para su funcionalidad independiente. Utiliza paho.mqtt.client para definir un cliente que puede enviar mensajes a un  canal específico.
Posee funciones definidas cuando envía y recibe un mensaje, para un mayor control de la comunicación del módulo y el servidor.
Actualmente se está utilizando la herramienta web CloudMqtt.com para observar la comunicación de los datos.
##  Flujo de Trabajo
El archivo test.py instancia un objecto de tipo Publisher y cada segundo envia datos de prueba al seridor MQTT hospedado en CloudMQTT.
Cuando el usuario desee terminar la ejecución de la aplicación solo deberá de presionar en la terminal CTRL+C para detener el hilo principal de la aplicación y el thread asociado de la clase publisher que cerrará la conexión.
##  Referencias

### Programación con hilos en Python
[Documentación oficial](https://docs.python.org/2/library/threading.html)
### Comunicación MQTT
[Documentación oficial](https://pypi.python.org/pypi/paho-mqtt/1.1#connect-reconnect-disconnect)