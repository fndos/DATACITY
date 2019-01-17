TraCI utiliza una arquitectura cliente / servidor basada en TCP para proporcionar acceso a SUMO.

Para realizar una simulación es necesario ejecutar sumo (servidor) con el siguiente comando
sumo -n osm.net.xml --remote-port 3345

Con este parametro se indica el número de clientes permitidos para la misma conexión
sumo -n osm.net.xml --remote-port 3345 --num-clients 100

Este comando realiza la simulación y exporta el archivo FCD (Output de SUMO)
Este comando no es necesario ejecutarlo puesto que está embebido en el archivo runner.py
Se debe ejecutar runner.py para realizar la simulación
sumo -c osm.sumocfg --fcd-output resclima_sumo_trace.xml

NOTA: En el directorio de SUMO deben estar el resto de archivos de configuracion para la simulacion
      No se subieron porque eran demasiado pesados.
