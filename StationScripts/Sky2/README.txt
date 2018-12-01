***** sky2.py *****
Es un script que se conecta a una base de datos,
y obtiene las variables, las estaciones de tipo
SKY2. Realiza las peticiones al API de BloomSky
y guarda las mediciones en la base de datos

****** Instalacion ******

Se debe copiar el archivo del servicio
en el directorio de systemd
$ sudo cp sky2.service /etc/systemd/system
$ cd /etc/systemd/system

Hay que habilitar el servicio
$ sudo systemctl enable sky2.service
 
Hay que empezar el servicio
$ sudo systemctl start sky2.service 

Para detener|empezar|reiniciar el servicio
$ sudo systemctl stop|start|restart sky2.service 

Para revisar el status del servicio
$ sudo systemctl status sky2.service

