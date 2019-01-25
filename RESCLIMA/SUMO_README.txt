Para la visualización hay que instalar matplotlib

TraCI utiliza una arquitectura cliente / servidor basada en TCP para proporcionar acceso a SUMO.

Para realizar una simulación es necesario ejecutar sumo (servidor) con el siguiente comando
Realizar en sumo-git/tools
sumo -n osm.net.xml --remote-port 8888

Con este parametro se indica el número de clientes permitidos para la misma conexión
sumo -n osm.net.xml --remote-port 8888 --num-clients 99

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

python plot_trajectories.py resclima_sumo_trace.xml -t td -o plot.png -s

INSTALACION DJANGO ADICIONAL
django_cleanup
celery-progress https://github.com/czue/celery-progress


python plot_dump_net.py -v -n bs.net.xml --xticks 7000,14001,2000,16 --yticks 9000,16001,1000,16 --measures entered,entered --xlabel [m] --ylabel [m] --default-width 1 -i base-jr.xml,base-jr.xml --xlim 7000,14000 --ylim 9000,16000 - --default-width .5 --default-color #606060 --min-color-value -1000 --max-color-value 1000 --max-width-value 1000 --min-width-value -1000 --max-width 3 --min-width .5 --colormap #0:#0000c0,.25:#404080,.5:#808080,.75:#804040,1:#c00000

Para procesar la salida instalar el siguiente paquete de python
pip install xmltodict
