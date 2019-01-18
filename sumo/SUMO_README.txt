Para la visualización hay que instalar matplotlib

TraCI utiliza una arquitectura cliente / servidor basada en TCP para proporcionar acceso a SUMO.

Para realizar una simulación es necesario ejecutar sumo (servidor) con el siguiente comando
Realizar en sumo-git/tools
sumo -n osm.net.xml --remote-port 3345

Con este parametro se indica el número de clientes permitidos para la misma conexión
sumo -n osm.net.xml --remote-port 3345 --num-clients 100

Este comando realiza la simulación y exporta el archivo FCD (Output de SUMO)
Este comando no es necesario ejecutarlo puesto que está embebido en el archivo runner.py
Se debe ejecutar runner.py para realizar la simulación
sumo -c osm.sumocfg --fcd-output resclima_sumo_trace.xml

A continuación se listan las posibles salidas de la simulacion

Raw Vehicle Position Dump
Contien cada arco y linea, cada una de las posiciones de los vehiculos y sus velocidades,
para cada step de la simulacion
sumo -c osm.sumocfg --netstate-dump resclima_dump_file.xml

Emission Output: Cantidad de CO2, CO, HC, NOX, fuel, electricity, noise, emitted
by the simulation
sumo -c osm.sumocfg --emission-output resclima_emission_file.xml

NOTA: En el directorio de SUMO deben estar el resto de archivos de configuracion para la simulacion
      No se subieron porque eran demasiado pesados.

python2 plot_trajectories.py resclima_sumo_trace.xml -t td -o plot.png -s

INSTALACION DJANGO ADICIONAL
django_cleanup
