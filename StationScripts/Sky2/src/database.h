#ifndef _DATABASE_H
#define	_DATABASE_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <libpq-fe.h>
#include "datastructs.h"

// Setea el archivo de configuracion
// que contiene las credenciales de la base de datos
// retorna cero si la operacion es correcta
int setConfigFile(char* fileName);

// Obtiene las estaciones desde
// la base de datos
// retorna un arreglo de punteros a 
// Station, definido en datastructs.h
// el ultimo elemento del arreglo es NULL
Station ** getStations(char * error);

// Obtiene las variables por alias
// desde la base de datos
// recibe un arreglo de strings con los alias de las variables
// y el numero de variables
// retorna un arreglo de punteros a 
// Variable, definido en datastructs.h
// el ultimo elemento del arreglo es NULL
Variable ** getVariablesByAliases(char** variables_aliases,int n,char * error);

// Guarda los datos en la base de datos
// Recibe un puntero a Measurements
// definido en datastructs.h
int insertMeasures(Measurements* m,char* error);

#endif	