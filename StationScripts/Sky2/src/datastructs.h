#ifndef _DATASTRUCTS_H
#define	_DATASTRUCTS_H

#include <stdio.h>
#include <time.h>

typedef struct Station{
    int id;
    char * token;
    float frequency;
}Station;

typedef struct Variable{
    char * id;
    char * alias;
    char * datatype;
}Variable;

typedef struct Measurements{
	int idStation;
	char * datetime;
	char * values;
}Measurements;

#endif