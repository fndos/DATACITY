# -*- encoding: utf-8 -*-
import xmltodict
import pprint
import json

from . utils import (
	get_average_emission,
	get_average_emission_by_type,
	get_average_trace,
	get_average_trace_by_type,
	get_summary,
	get_key_value_emission_by_type
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
	data = []
	vehicle_list = []
	for step in step_list:
		vehicle_list.append(step['vehicle'])
	for v in vehicle_list:
		for x in v:
			# Obtengo cada linea de vehiculo del timestep
			data.append({'vehicle': x})
	# Realizar las funciones de acumulacion, average, etc.
	AVG_EMISSION_DICT = get_average_emission(data)
	AVG_WEIGHT_EMISSION_DICT, AVG_LIGHT_EMISSION_DICT = get_average_emission_by_type(data)
	KEY_VALUE_WEIGHT_CO2_DICT, KEY_VALUE_LIGHT_CO2_DICT= get_key_value_emission_by_type(vehicle_list, "CO2")
	KEY_VALUE_WEIGHT_CO_DICT, KEY_VALUE_LIGHT_CO_DICT = get_key_value_emission_by_type(vehicle_list, "CO")
	return AVG_EMISSION_DICT, AVG_WEIGHT_EMISSION_DICT, AVG_LIGHT_EMISSION_DICT, KEY_VALUE_WEIGHT_CO2_DICT, KEY_VALUE_LIGHT_CO2_DICT, KEY_VALUE_WEIGHT_CO_DICT, KEY_VALUE_LIGHT_CO_DICT

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
	data = []
	vehicle_list = []
	for step in step_list:
		vehicle_list.append(step['vehicle'])
	for v in vehicle_list:
		for x in v:
			# Obtengo cada linea de vehiculo del timestep
			data.append({'vehicle': x})
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
