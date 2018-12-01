# encoding: utf-8
from utils import parseUserTextInput, create_str_polygon_postgis;


def getTsTextQuery(query_object):
	#query object fields : text, polygon, startDate, endDate
	params = []
	
	# sql statements
	select_stm = 'SELECT v."id", v."name", array_agg(s.id) as stations, count(*) OVER() AS full_count '
	from_stm = 'FROM "timeSeries_variable" as v, "timeSeries_stationtype" as st, "timeSeries_station" as s, "timeSeries_stationtype_variables" as st_v '
	# JOIN entre station y stationType 
	where_stm = 'WHERE s."stationType_id" = st."id" AND '
	# JOIN entre stationType y la tabla intermedia (station_type_variables)
	where_stm = where_stm + 'st."id" = st_v."stationtype_id" AND '
	# JOIN entre tabla intermedia (station_type_variables) y variable
	where_stm = where_stm + 'st_v."variable_id" = v."id" '
	
	# si hay bbox
	if(query_object.has_key("bbox")):
		bbox_str = create_str_polygon_postgis(query_object["bbox"])
		if bbox_str == None:
			return "Error"
		where_stm = where_stm + 'AND ST_Intersects(s."location", %s)'
		params.append(bbox_str)

	# is hay fechas de inicio y fin
	if(query_object.has_key("ini") and query_object.has_key("end")):
		""" startDate and endDate are datetime instances
		"""
		#startDateStr = query_object["ini"].strftime("%Y-%m-%d %H:%M:%S")
		#endDateStr = query_object["end"].strftime("%Y-%m-%d %H:%M:%S")
		startDateStr = query_object["ini"]
		endDateStr = query_object["end"]
		where_stm = where_stm + 'AND EXISTS ( SELECT m."idStation_id" FROM "timeSeries_measurement" as m WHERE m."ts">=%s AND m."ts" <= %s AND m."idStation_id" = s.id) '
		params.append(startDateStr)
		params.append(endDateStr)
	else:
		where_stm = where_stm + 'AND EXISTS ( SELECT m."idStation_id" FROM "timeSeries_measurement" as m WHERE m."idStation_id" = s.id) '

	# si hay texto
	if(query_object.has_key("text") or query_object.has_key("categories") ):
		#check if the user entered a text or categories to the search
		text = query_object.get("text","")
		categories = query_object.get("categories", [])
		if(text or len(categories)>0):
			ts_query_str = parseUserTextInput(text,categories);
			where_stm = where_stm + 'AND v."ts_index" @@ to_tsquery(\'spanish\', %s) '
			params.append(ts_query_str)
	
	qs = select_stm + from_stm + where_stm
	qs = qs + 'GROUP BY  v.id '


	limit = query_object.get("limit",None)
	offset = query_object.get("offset",None)
	
	if(limit!=None and offset!=None):
		qs = qs + " LIMIT %s OFFSET %s"
		params.append(limit)
		params.append(offset)

	print("EL QUERY DE BUSQUEDA  "+ qs)
	return qs, params




