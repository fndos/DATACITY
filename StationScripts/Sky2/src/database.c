#include "database.h"
#include <jansson.h>

char CONFIG_FILE_NAME[150];

int setConfigFile(char* fileName){
	if(!fileName){
		return -1;
	}
	strcpy(CONFIG_FILE_NAME,fileName);
	return 0;
}

PGconn * _connect(){

	json_t* source, *p1,*p2,*p3;
    json_error_t error;
    // lee el archivo de configuracion
    source = json_load_file(CONFIG_FILE_NAME,0,&error);
    if(!source){
    	return NULL;
    }
    if(!json_is_object(source)){
    	return NULL;
    }
    p1 = json_object_get(source,"dbname");
    if(!p1) return NULL;
    const char * dbname = json_string_value(p1);

    p2 = json_object_get(source,"user");
    if(!p2) return NULL;
    const char * user = json_string_value(p2);

    p3 = json_object_get(source,"password");
    if(!p3) return NULL;
    const char * password = json_string_value(p3);


    char * conection_string = (char*)malloc(sizeof(char)*150);
    sprintf(conection_string,"hostaddr='127.0.0.1' port=5432 dbname=%s user=%s password=%s",dbname,user,password);
	PGconn *conn = PQconnectdb(conection_string);

	json_decref(source);
	json_decref(p1);
	json_decref(p2);
	json_decref(p3);
	free(conection_string);

    if (PQstatus(conn) == CONNECTION_BAD) {
        return NULL;
    }
    return conn;
}

Station ** getStations(char * error){
    Station ** stations = NULL;
    PGconn *conn = _connect();
    if(!conn){
    	strcpy(error,"No se pudo conectar a la base de datos estaciones");
    	PQfinish(conn);
    	return NULL;
    }
    char query[] = "SELECT s.id,s.token,s.frequency "
                   "FROM \"TimeSeries_station\" as s, "  
                   "\"TimeSeries_stationtype\" as st "
                   "WHERE st.brand='BloomSky' and st.model='SKY2' "
                    "and \"stationType_id\"=st.id";

    PGresult *res = PQexec(conn,query);    
    
    if (PQresultStatus(res) != PGRES_TUPLES_OK) {
        strcpy(error,"Error en el query");        
        PQclear(res);
    	PQfinish(conn);
    	return NULL;
    }   
    
    int rows = PQntuples(res);
    
    if(rows<=0){
        strcpy(error,"No se recuperaron estaciones");
        PQclear(res);
    	PQfinish(conn);
    	return NULL;
    }

    int size = (sizeof(Station*))*(rows+1);
    stations = (Station**)malloc(size);
    if(!stations){
    	strcpy(error,"Error en malloc: No hay memoria");
    	PQclear(res);
    	PQfinish(conn);
        return NULL;
    }

    for(int i=0; i<rows; i++) {
        int idStation = atoi(PQgetvalue(res, i, 0)); 
        char * token  = PQgetvalue(res, i, 1);
        float frequency = atof(PQgetvalue(res, i, 2));
        Station* station = (Station*)malloc(sizeof(Station));
        if(!station){
        	strcpy(error,"Error en malloc: No hay memoria");
        	PQclear(res);
    		PQfinish(conn);
        	return NULL;
        }
        station->id = idStation;
        station->token = token;
        station->frequency = frequency;
        stations[i] = station;
    }
    PQclear(res);
    PQfinish(conn);
    stations[rows]=NULL;
    return stations;
}

Variable * _getVariableByAlias(char* variable_alias,char* error){
	
	if(!variable_alias){
		strcpy(error,"Error de argumento de _getVariableByAlias");
		return NULL;
	}

	PGconn *conn = _connect();

	if(!conn){
    	sprintf(error,"No se pudo conectar a la base de datos alias %s",variable_alias);
    	PQfinish(conn);
    	return NULL;
    }

    char query[] = "SELECT v.id,v.alias,v.datatype "
                   "FROM \"TimeSeries_variable\" as v "  
                   "WHERE v.alias=$1";

    const char *values[1] = {variable_alias};
    int lengths[1] = {strlen(variable_alias)};
    int binary[1] = {0};

    PGresult *res = PQexecParams(conn,query,1,NULL,values,lengths,binary,0);
    
    if (PQresultStatus(res) != PGRES_TUPLES_OK) {
       	strcpy(error,"Error en el query");        
        PQclear(res);
    	PQfinish(conn);
    	return NULL;
    }   
    
    int rows = PQntuples(res);
    
    if(rows<=0){
    	sprintf(error,"No se encontro la variable %s",variable_alias);        
        PQclear(res);
    	PQfinish(conn);
        return NULL;
    }
    Variable* variable = (Variable*)malloc(sizeof(Variable));
    if(!variable){
    	strcpy(error,"Error en malloc: No hay memoria");        
        PQclear(res);
    	PQfinish(conn);
        return NULL;	
    }
    char * id = (char*)malloc(sizeof(char)*50);
    if(!id){
    	strcpy(error,"Error en malloc: No hay memoria");        
        PQclear(res);
    	PQfinish(conn);
        return NULL;
    }
    strcpy(id,PQgetvalue(res, 0, 0));
    variable->id = id;
    char * alias = (char*)malloc(sizeof(char)*50);
    if(!alias){
    	strcpy(error,"Error en malloc: No hay memoria");        
        PQclear(res);
    	PQfinish(conn);
        return NULL;
    }
    strcpy(alias,PQgetvalue(res, 0, 1));
    variable->alias = alias;
    char * datatype = (char*)malloc(sizeof(char)*20);
    if(!datatype){
    	strcpy(error,"Error en malloc: No hay memoria");        
        PQclear(res);
    	PQfinish(conn);
        return NULL;
    }
    strcpy(datatype,PQgetvalue(res, 0, 2));
    variable->datatype = datatype;
    PQclear(res);
    PQfinish(conn);

    return variable;
}

Variable ** getVariablesByAliases(char** variables_aliases,int n,char * error){
	Variable ** variables = NULL;
	int size = (sizeof(Variable*))*(n+1);
	variables = (Variable**)malloc(size);
	if(!variables){
		strcpy(error,"Error en malloc: No hay memoria");
		return NULL;
	}
    char variable_alias[50];
    int i;
    for(i=0;i<n;i++){
    	strcpy(variable_alias,variables_aliases[i]);
    	Variable* variable = _getVariableByAlias(variable_alias,error);
    	if(!variable){
    		return NULL;
    	}
    	variables[i]=variable;
    }
    variables[n]=NULL;
    return variables;
}

int insertMeasures(Measurements* m,char* error){
	PGconn *conn = _connect();
    if(!conn){
        strcpy(error,"No se pudo conectar a la base de datos medidas");
        PQfinish(conn);
        return -1;
    }
    // se preparan los parametros del query
    int idStation = htonl(m->idStation);
	char * datetime = m->datetime;
	printf("%s\n",datetime);
	char * readings = m->values;

    char query[] = "SELECT InsertSky2Measurements($1::integer,$2::timestamp,$3::json)";
    printf("%s\n",query);
    const char *values[3];
    values[0] = (char *)&idStation;
    values[1] = datetime;
    values[2] = readings;
    int lengths[3] = {sizeof(idStation),strlen(datetime),strlen(readings)};
    int binary[3] = {1,0,0};
    printf("Parametros correctos\n");
    PGresult *res = PQexecParams(conn,query,3,NULL,values,lengths,binary,0);
    printf("Corrio el query\n");
    if (PQresultStatus(res) != PGRES_TUPLES_OK) {
        printf("Error en el query\n");
        strcpy(error,"Error en el query");
        // se puede llamar a esta funcion PQerrorMessage() 
        // para tener mas informacion del error
        printf("%s\n",PQerrorMessage(conn));         
        PQclear(res);
    	PQfinish(conn);
    	return -1;
    }
    printf("Query correcto\n");
    PQclear(res);
    PQfinish(conn);
    printf("Funcion correcta\n"); 
    return 0;
}