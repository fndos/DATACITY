#ifndef _REQUEST_H
#define _REQUEST_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

// Configura la libreria libcurl
// Retorna cero si la operacion fue correcta
int configRequest();

// Extrae los datos de una estacion sky2
// mediante el API. Recibe el token
// de autenticacion.
// Retorna la respuesta en un string
char* getSKY2Data(char* token);


#endif
