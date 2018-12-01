#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <pthread.h>
#include <signal.h>
#include <unistd.h>
#include <syslog.h> 
#include <curl/curl.h>
#include <jansson.h>
#include "datastructs.h"
#include "database.h"
#include "request.h"

// gcc -o sky2Adapter sky2Adapter.c database.c request.c -I/usr/include/postgresql -I/usr/local/include -L/usr/local/lib -lpthread -lcurl -lpq -ljansson
// tdbDpM7ktbTRos6iv3C76dQ=

//curl-7.61.0
//jansson-2.11

Measurements* parseMeasurements(int idStation,char* data_json, Variable** variables);
void* dataExtraction_thread(void* arg);

typedef struct Thread_arg{
    Station* station;
    Variable** variables;
}Thread_arg;

// bandera de terminacion de hilos
int finish_flag = 0;
FILE * BACKUP_FILE; // archivo de backup
//variable de condicion
pthread_cond_t finish_cv = PTHREAD_COND_INITIALIZER;
// mutex para el cv
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
// mutex para el archivo de log
pthread_mutex_t mutex_log = PTHREAD_MUTEX_INITIALIZER;
// mutex para el archivo de backup
pthread_mutex_t mutex_backup = PTHREAD_MUTEX_INITIALIZER;

// handler para cerrar el programa
void _exit(int value){
    printf("\nProceso terminado\n");
    fclose(LOG_FILE);
    fclose(BACKUP_FILE);
    exit(value);
}

char * ident = "sky2";

void _log(char * msg){
/*    time_t t = time(NULL);
    struct tm * utc_tm = gmtime(&t);
    char datetime_str[20];
    strftime(datetime_str,20,"%Y-%m-%d %H:%M:%S", utc_tm);
    pthread_mutex_lock(&mutex_log);
    fprintf(LOG_FILE,"%s\t%s\n",datetime_str,msg);
    pthread_mutex_unlock(&mutex_log);*/
    openlog(ident, LOG_PID|LOG_CONS, LOG_USER);
    syslog(LOG_INFO, msg);
    closelog();
}

void _backup(char* data){
    pthread_mutex_lock(&mutex_backup);
    fprintf(BACKUP_FILE,"%s\n",data);
    pthread_mutex_unlock(&mutex_backup);
}

int main(int argc, char* argv[]) {
    // se lee el nombre del archivo de configuracion
    char * configFileName = "/home_local/obayona/Documents/RESCLIMA/StationScripts/Sky2/config.json";
    char * logFileName = "/home_local/obayona/Documents/RESCLIMA/StationScripts/Sky2/log.txt";
    char * backupFileName = "/home_local/obayona/Documents/RESCLIMA/StationScripts/Sky2/backup.txt";
    // se registran los signal
    printf("%s %s %s",configFileName,logFileName,backupFileName);
    signal(SIGINT, _exit);
    //signal(SIGSEGV,_exit);

    // configura el modulo de la base de datos
    int code = setConfigFile(configFileName);    
    if(code!=0){ 
        _log("Error en el archivo de configuracion");
        return -1;
    }
    // se configura la libreria de request
    code = configRequest();
    if(code!=0){ 
        _log("Error en inicializar libcurl");
        return -1;
    }
    BACKUP_FILE = fopen(backupFileName,"a");
    if(!LOG_FILE){
        _log("No existe el archivo de backup");
        return -1;
    }

    // se crea el arreglo de alias
    // de las variables
    char *variables_aliases[3]={'\0'};
    variables_aliases[0]="Luminance";
    variables_aliases[1]="Temperature";
    variables_aliases[2]="Humidity";

    // se extraen las variables de
    // de la base de datos
    char errorMsg[100];
    Variable ** variables = getVariablesByAliases(variables_aliases,3,errorMsg);
    if(!variables){
        _log(errorMsg);
        _exit(-1);
    }

    // Se obtienen las estaciones SKY2 de 
    // la base de datos
    Station ** stations = getStations(errorMsg);
    if(!stations){
        _log(errorMsg);
        _exit(2);
    }
    // por cada estacion se crea un hilo
    Station ** iter = stations;
    while(*iter){
        Thread_arg * args = (Thread_arg*)malloc(sizeof(Thread_arg));
        if(!args){
            _log("Error en el malloc");
            _exit(-1);
        }
        args->station = *iter;
        args->variables = variables;
        pthread_t thread;
        pthread_create(&thread, NULL, dataExtraction_thread, args);
        iter++;
    }
    // se duerme el main por siempre
    // la variable de condicion nunca es 
    // activada
    pthread_mutex_lock(&mutex);
    while(finish_flag==0){
        pthread_cond_wait(&finish_cv, &mutex);
    }
    pthread_mutex_unlock(&mutex);

    // cerrar todo
    fclose(LOG_FILE);
    return 0;
}


Measurements* parseMeasurements(int idStation,char* data_json, Variable** variables){
    json_t* array, * source,*measurements, *object, *result;
    json_error_t error;


    array = json_loads(data_json,0,&error);
    if(!array){
        return NULL;
    }
    if(!json_is_array(array)){
        json_decref(array);
        return NULL;
    }
    //source = json_load_file("result.txt",0,&error);
    source = json_array_get(array,0);
    if(!source){
        json_decref(array);
        return NULL;
    }
    if(!json_is_object(source)){
        json_decref(array);
        return NULL;
    }
    // json con resultados
    result = json_object();
    if(!result){
        json_decref(array);
        return NULL;
    }

    measurements = json_object_get(source,"Data");
    if(!measurements){
        json_decref(array);
        return NULL;
    }
    if(!json_is_object(measurements)){
        json_decref(array);
        return NULL;
    }

    object = json_object_get(measurements,"TS");
    if(!object){
        json_decref(array);
        return NULL;
    }
    if(!json_is_integer(object)){
        json_decref(array);
        return NULL;
    }
    const time_t utc_time = (const time_t)json_integer_value(object);
    struct tm * utc_tm = gmtime(&utc_time); 
    char * datetime_str = (char*)malloc(sizeof(char)*20);
    strftime(datetime_str,20,"%Y-%m-%d %H:%M:%S",utc_tm);

    Variable** iter = variables;
    while(*iter){
        Variable* variable = *iter;
        char * id = variable->id;
        char * alias = variable->alias;
        char * datatype = variable->datatype;
        object = json_object_get(measurements,alias);
        if(!object){
            json_decref(array);
            return NULL;
        }
        json_object_set(result,id,object); 
        iter++;
    }

    char* values_str = json_dumps(result,0);
    json_decref(array);
    json_decref(result);

    Measurements* m = (Measurements*)malloc(sizeof(Measurements));
    m->idStation = idStation;
    m->datetime = datetime_str;
    m->values = values_str;

    return m;
}


void* dataExtraction_thread(void* arg){
    // se extraen los argumentos
    Thread_arg* args = (Thread_arg*)arg;
    Station * station = args->station;
    Variable** variables = args->variables;
    // frecuencua en minutos
    int frecuency = station->frequency;
    int segundos = frecuency*1;
    int idStation = station->id;
    char token[30];
    char logMsg[100];
    strcpy(token,station->token);
    int cont = 0;
    while(1){
        // se duerme el hilo
        sleep(segundos);
        printf("%d\n",cont);
        sprintf(logMsg,"Descarga datos cada %d segundos de la estacion %d",segundos,idStation);
        _log(logMsg);
        // se traen los datos a traves del API
        char * data = getSKY2Data(token);
        printf("Datos descargados\n");
        if(!data){
            sprintf(logMsg,"No se pueden traer los datos de la estacion %d",idStation);
            _log(logMsg);
            continue;
        }
        // se parsean los datos
        printf("Datos no nulos\n");
        Measurements* m = parseMeasurements(idStation,data,variables);
        printf("Datos parseados\n");
        if(!m){
            sprintf(logMsg,"Error de parseo en los datos de la estacion %d",idStation);
            _log(logMsg);
            free(data);
            continue;   
        }
        printf("Datos bien parseados\n");
        // se guardan los datos en la base de datos
        int result = insertMeasures(m,logMsg);
        printf("Datos guardados\n");
        if(result!=0){
            _log(logMsg);
            // se intenta guardar en un archivo de backup
            _backup(data);
        }
        printf("Datos guardados correctamente\n");
        free(data);
        free(m->datetime);
        free(m->values);
        free(m);
        printf("Memoria liberada\n");
        cont ++;
    }

}