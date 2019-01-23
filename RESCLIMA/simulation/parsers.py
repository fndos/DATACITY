# -*- encoding: utf-8 -*-
import xmltodict
import pprint
import json

from . utils import (
	get_average_emission,
	get_average_emission_by_type,
	get_average_trace,
	get_average_trace_by_type,
	get_summary
)

def emission_parser(path):
	with open(path) as fd:
	    doc = xmltodict.parse(fd.read())
	# JSON Parser
	json_string=json.dumps(doc)
	data = json.loads(json_string)
	# Obtengo el reporte de emisiones
	emission_export = data['emission-export']
	# Obtengo una lista de los timestep del reporte
	step_list = emission_export['timestep']
	# Itero dentro de cada timestep
	for step in step_list:
		# Obtengo cada linea de vehiculo del timestep
		vehicle_list = step['vehicle']
	data = [{'vehicle': x } for x in vehicle_list]
	# Realizar las funciones de acumulacion, average, etc.
	AVG_EMISSION_DICT = get_average_emission(data)
	AVG_WEIGHT_EMISSION_DICT, AVG_LIGHT_EMISSION_DICT = get_average_emission_by_type(data)
	return AVG_EMISSION_DICT, AVG_WEIGHT_EMISSION_DICT, AVG_LIGHT_EMISSION_DICT

def trace_parser(path):
	with open(path) as fd:
	    doc = xmltodict.parse(fd.read())
	# JSON Parser
	json_string=json.dumps(doc)
	data = json.loads(json_string)
	# Obtengo el reporte de emisiones
	trace_export = data['fcd-export']
	# Obtengo una lista de los timestep del reporte
	step_list = trace_export['timestep']
	# Itero dentro de cada timestep
	for step in step_list:
		# Obtengo cada linea de vehiculo del timestep
		vehicle_list = step['vehicle']
	data = [{'vehicle': x } for x in vehicle_list]
	# Realizar las funciones de acumulacion, average, etc.
	AVG_TRACE_DICT = get_average_trace(data)
	AVG_WEIGHT_TRACE_DICT, AVG_LIGHT_TRACE_DICT = get_average_trace_by_type(data)
	return AVG_TRACE_DICT, AVG_WEIGHT_TRACE_DICT, AVG_LIGHT_TRACE_DICT

def summary_parser(path):
	with open(path) as fd:
	    doc = xmltodict.parse(fd.read())
	# JSON Parser
	json_string=json.dumps(doc)
	data = json.loads(json_string)
	# Obtengo el reporte de emisiones
	summary = data['summary']
	# Obtengo una lista de los timestep del reporte
	step_list = summary['step']
	# Obtengo cada linea de step en summary
	data = [{'step': x } for x in step_list]
	# Realizar las funciones de acumulacion, average, etc.
	SUMMARY_DICT = get_summary(data)
	return SUMMARY_DICT
