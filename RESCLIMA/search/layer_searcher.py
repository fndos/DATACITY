# encoding: utf-8
from utils import parseUserTextInput, create_str_polygon_postgis;


# Genera un query dinamico dependiendo
# de las opciones de query_object
def create_query(query_object):
	# opciones de busqueda
	text = query_object.get("text","")
	categories = query_object.get("categories", [])
	bbox = query_object.get("bbox", None)
	ini_date = query_object.get("ini_date",None)
	end_date = query_object.get("end_date",None)
	limit = query_object.get("limit",None)
	offset = query_object.get("offset",None)

	# sql statements
	select_stm = 'SELECT l.id, l.title, l.abstract, l.type, l.bbox, count(*) OVER() AS full_count';

	from_stm = 'FROM "layer_layer" AS l';
	where_stm = 'WHERE';
	where_filters = [];
	params = []

	if(text or len(categories)>0):
		ts_query_str = parseUserTextInput(text,categories);
		filter_str = 'ts_index @@ to_tsquery(\'spanish\',%s)'
		where_filters.append(filter_str);
		params.append(ts_query_str);


	if(bbox):
		bbox_str = create_str_polygon_postgis(bbox);
		if bbox_str == None:
			return "Error";
		filter_str = 'ST_Intersects(bbox,%s)';
		where_filters.append(filter_str);
		params.append(bbox_str);

	if(ini_date and end_date):
		filter_str = 'data_date >= %s and data_date <= %s';
		where_filters.append(filter_str)
		params.append(ini_date);
		params.append(end_date);

	sql_query = select_stm;
	sql_query = sql_query + " " + from_stm
	sql_query = sql_query + " " + where_stm

	for i,f in enumerate(where_filters):
		if (i==0):
			sql_query = sql_query + " " + f
		else:
			sql_query = sql_query + " and " + f

	sql_query= sql_query + " ORDER BY data_date"

	if(limit!=None and offset!=None):
		sql_query = sql_query + " LIMIT %s OFFSET %s"
		params.append(limit)
		params.append(offset)

	print sql_query, params
	return sql_query, params

