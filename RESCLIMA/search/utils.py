import re

def create_str_polygon_postgis(polygon_dict):
	minX = polygon_dict["minX"];
	maxX = polygon_dict["maxX"];
	minY = polygon_dict["minY"];
	maxY = polygon_dict["maxY"];
	if (minX=='0' and maxX=='0' and minY=='0' and maxY=='0'):
		return None
	else:
		polygon_str = "SRID=4326;POLYGON((%s %s,%s %s,%s %s,%s %s,%s %s))::geometry"%(float(minX),float(minY),float(minX),float(maxY),float(maxX),float(maxY),float(maxX),float(minY),float(minX),float(minY));
		return polygon_str

def parseUserTextInput(text,categories):
	pattern = re.compile(r'\w+',re.UNICODE)
	tokens = re.findall(pattern, text)
	ts_query_str = ""
	num_tokens = len(tokens)
	for index, token in enumerate(tokens):
		if(index != num_tokens - 1):
			token += " | "
		ts_query_str += token

	num_categories = len(categories)
	if num_categories==0:
		return ts_query_str

	if(num_tokens>0):
		ts_query_str += " | ("

	for index, category in enumerate(categories):
		category = category.replace(" ","|")
		if(index != num_categories - 1):
			category += " | "
		ts_query_str += category

	if(num_tokens>0):
		ts_query_str += ")"

	return ts_query_str


