# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from timeSeries import models
from simulation import models as simulation_models
from main import models as main_models
from . import serializers

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

import json

# Grafico de barras para los investigadores de ESPOL
# Response format: {key, value}
class Medicion(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		# Obtener el diccionario para las variables
		qs = models.Variable.objects.all()
		dict = {}
		v = list(qs)
		for i in range(len(v)):
			dict[i] = v[i].name
		# Obtener las lecturas de las estaciones por timestamp
		try:
			if start_date == "null" or end_date == "null":
				# qs no debe incluir fechas
				qs = models.Measurement.objects.raw('''SELECT * FROM \"timeSeries_measurement\"''');
			else:
				qs = models.Measurement.objects.raw('''SELECT * FROM \"timeSeries_measurement\" WHERE ts <= %s::DATE AND ts >= %s::DATE''', [end_date, start_date]);
			ms = list(qs)
			avg = [0] * 9
			# Agrupo por id de variable.
			for i in range(len(ms)):
				r = json.loads(ms[i].readings)
				avg[0] = avg[0] + r["1"] # Temperatura
				avg[1] = avg[1] + r["2"] # Humedad Relativa
				avg[2] = avg[2] + r["3"] # Lluvia
				avg[3] = avg[3] + r["4"] # Direccion del viento
				avg[4] = avg[4] + r["5"] # Velocidad del viento
				avg[5] = avg[5] + r["6"] # Velocidad de rafagas
				avg[6] = avg[6] + r["7"] # Luminancia
				avg[7] = avg[7] + r["10"] # Presión
				avg[8] = avg[8] + r["11"] # Indice UV
			# Aplico el promedio
			for i in range(len(avg)):
				avg[i] = avg[i] / len(ms)
			# Reemplazo el id por dict para que se pueda ver el nombre
			content = [{"value":avg[0], "key":dict[0]},
					   {"value":avg[1], "key":dict[1]},
					   {"value":avg[2], "key":dict[2]},
					   {"value":avg[3], "key":dict[3]},
					   {"value":avg[4], "key":dict[4]},
					   {"value":avg[5], "key":dict[5]},
					   {"value":avg[6], "key":dict[6]},
					   {"value":avg[7], "key":dict[9]},
					   {"value":avg[8], "key":dict[10]},
					  ]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Grafico circular para los investigadores de logsitica y transporte
# Response format: {key, value}
class WE(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, sid=None):
		# Como ingresar parametros al API
		try:
			output_instance = simulation_models.Output.objects.get(simulation__id=sid)
			CO2 = output_instance.avg_weight_emission[1]['CO2']
			CO = output_instance.avg_weight_emission[2]['CO']
			PMx = output_instance.avg_weight_emission[3]['PMx']
			NOx = output_instance.avg_weight_emission[4]['NOx']
			HC = output_instance.avg_weight_emission[5]['HC']

			# Formatter
			CO2 = str("{0:.2f}".format(CO2))
			CO = str("{0:.2f}".format(CO))
			PMx = str("{0:.2f}".format(PMx))
			NOx = str("{0:.2f}".format(NOx))
			HC = str("{0:.2f}".format(HC))

			# Generar respuesta JSON
			content = [{"value":float(CO2), "key":"CO2"},
				       {"value":float(CO), "key":"CO"},
					   {"value":float(PMx), "key":"PMx"},
   				       {"value":float(NOx), "key":"NOx"},
   				       {"value":float(HC), "key":"HC"}
					  ]

		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Response format: {key, value}
class LE(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, sid=None):
		# Como ingresar parametros al API
		try:
			output_instance = simulation_models.Output.objects.get(simulation__id=sid)
			CO2 = output_instance.avg_light_emission[1]['CO2']
			CO = output_instance.avg_light_emission[2]['CO']
			PMx = output_instance.avg_light_emission[3]['PMx']
			NOx = output_instance.avg_light_emission[4]['NOx']
			HC = output_instance.avg_light_emission[5]['HC']

			# Formatter
			CO2 = str("{0:.2f}".format(CO2))
			CO = str("{0:.2f}".format(CO))
			PMx = str("{0:.2f}".format(PMx))
			NOx = str("{0:.2f}".format(NOx))
			HC = str("{0:.2f}".format(HC))

			# Generar respuesta JSON
			content = [{"value":float(CO2), "key":"CO2"},
				       {"value":float(CO), "key":"CO"},
					   {"value":float(PMx), "key":"PMx"},
   				       {"value":float(NOx), "key":"NOx"},
   				       {"value":float(HC), "key":"HC"}
					  ]

		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Grafico de lineas para los investigadores de logistica y transporte
# Response format: {key, value}
class WMS(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, sid=None):
		try:
			output_instance = simulation_models.Output.objects.get(simulation__id=sid)
			content = output_instance.key_value_weight_mean_speed
		except simulation_models.Output.DoesNotExist:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Response format: {key, value}
class LMS(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, sid=None):
		try:
			output_instance = simulation_models.Output.objects.get(simulation__id=sid)
			content = output_instance.key_value_light_mean_speed
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Response format: {key, value}
class WWT(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, sid=None):
		try:
			output_instance = simulation_models.Output.objects.get(simulation__id=sid)
			content = output_instance.key_value_weight_waiting
		except simulation_models.Output.DoesNotExist:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Response format: {key, value}
class LWT(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, sid=None):
		try:
			output_instance = simulation_models.Output.objects.get(simulation__id=sid)
			content = output_instance.key_value_light_waiting
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Grafico de barras para los investigadores de logistica y transporte (livianos)
# Descripcion: Circulacion de vehiculos livianos en GD sentido E-N
# Response format: {key, value}
class LEN(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		try:
			# Obtener la informacion de la BD
			if start_date == "null" or end_date == "null":
				# qs no debe incluir fechas
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE vehicle_type = 1 AND movement = 1''', [end_date, start_date])
			else:
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE date >= %s AND date <= %s AND vehicle_type = 1 AND movement = 1''', [end_date, start_date])

			d = list(qs)
			dict = {}
			for i in range(len(d)):
				dict[d[i].id_term] = d[i].value

			# Crear JSON dinamico
			content = [{"value": v, "key": k } for k, v in dict.iteritems()]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Descripcion: Circulacion de vehiculos livianos en FR Sentido E-O
# Response format: {key, value}
class LEO(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		try:
			# Obtener la informacion de la BD
			if start_date == "null" or end_date == "null":
				# qs no debe incluir fechas
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE vehicle_type = 1 AND movement = 2''', [end_date, start_date])
			else:
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE date >= %s AND date <= %s AND vehicle_type = 1 AND movement = 2''', [end_date, start_date])

			d = list(qs)
			dict = {}
			for i in range(len(d)):
				dict[d[i].id_term] = d[i].value

			# Crear JSON dinamico
			content = [{"value": v, "key": k } for k, v in dict.iteritems()]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Descripcion: Circulacion de vehiculos livianos en GD Sentido N-O
# Response format: {key, value}
class LNO(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		try:
			# Obtener la informacion de la BD
			if start_date == "null" or end_date == "null":
				# qs no debe incluir fechas
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE vehicle_type = 1 AND movement = 3''', [end_date, start_date])
			else:
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE date >= %s AND date <= %s AND vehicle_type = 1 AND movement = 3''', [end_date, start_date])

			d = list(qs)
			dict = {}
			for i in range(len(d)):
				dict[d[i].id_term] = d[i].value

			# Crear JSON dinamico
			content = [{"value": v, "key": k } for k, v in dict.iteritems()]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Descripcion: Circulacion de vehiculos livianos en GI Sentido O-N
# Response format: {key, value}
class LON(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		try:
			# Obtener la informacion de la BD
			if start_date == "null" or end_date == "null":
				# qs no debe incluir fechas
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE vehicle_type = 1 AND movement = 4''', [end_date, start_date])
			else:
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE date >= %s AND date <= %s AND vehicle_type = 1 AND movement = 4''', [end_date, start_date])

			d = list(qs)
			dict = {}
			for i in range(len(d)):
				dict[d[i].id_term] = d[i].value

			# Crear JSON dinamico
			content = [{"value": v, "key": k } for k, v in dict.iteritems()]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Descripcion: Circulacion de vehiculos livianos en FR Sentido O-E
# Response format: {key, value}
class LOE(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		try:
			# Obtener la informacion de la BD
			if start_date == "null" or end_date == "null":
				# qs no debe incluir fechas
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE vehicle_type = 1 AND movement = 5''', [end_date, start_date])
			else:
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE date >= %s AND date <= %s AND vehicle_type = 1 AND movement = 5''', [end_date, start_date])

			d = list(qs)
			dict = {}
			for i in range(len(d)):
				dict[d[i].id_term] = d[i].value

			# Crear JSON dinamico
			content = [{"value": v, "key": k } for k, v in dict.iteritems()]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Descripcion: Circulacion de vehiculos livianos en GI Sentido N-E
# Response format: {key, value}
class LNE(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		try:
			# Obtener la informacion de la BD
			if start_date == "null" or end_date == "null":
				# qs no debe incluir fechas
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE vehicle_type = 1 AND movement = 6''', [end_date, start_date])
			else:
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE date >= %s AND date <= %s AND vehicle_type = 1 AND movement = 6''', [end_date, start_date])

			d = list(qs)
			dict = {}
			for i in range(len(d)):
				dict[d[i].id_term] = d[i].value

			# Crear JSON dinamico
			content = [{"value": v, "key": k } for k, v in dict.iteritems()]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Grafico de barras para los investigadores de logistica y transporte (livianos)
# Descripcion: Circulacion de vehiculos pesados en GD sentido E-N
# Response format: {key, value}
class WEN(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		try:
			# Obtener la informacion de la BD
			if start_date == "null" or end_date == "null":
				# qs no debe incluir fechas
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE vehicle_type = 0 AND movement = 1''', [end_date, start_date])
			else:
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE date >= %s AND date <= %s AND vehicle_type = 0 AND movement = 1''', [end_date, start_date])

			d = list(qs)
			dict = {}
			for i in range(len(d)):
				dict[d[i].id_term] = d[i].value

			# Crear JSON dinamico
			content = [{"value": v, "key": k } for k, v in dict.iteritems()]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Descripcion: Circulacion de vehiculos pesados en FR Sentido E-O
# Response format: {key, value}
class WEO(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		try:
			# Obtener la informacion de la BD
			if start_date == "null" or end_date == "null":
				# qs no debe incluir fechas
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE vehicle_type = 0 AND movement = 2''', [end_date, start_date])
			else:
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE date >= %s AND date <= %s AND vehicle_type = 0 AND movement = 2''', [end_date, start_date])

			d = list(qs)
			dict = {}
			for i in range(len(d)):
				dict[d[i].id_term] = d[i].value

			# Crear JSON dinamico
			content = [{"value": v, "key": k } for k, v in dict.iteritems()]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Descripcion: Circulacion de vehiculos pesados en GD Sentido N-O
# Response format: {key, value}
class WNO(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		try:
			# Obtener la informacion de la BD
			if start_date == "null" or end_date == "null":
				# qs no debe incluir fechas
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE vehicle_type = 0 AND movement = 3''', [end_date, start_date])
			else:
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE date >= %s AND date <= %s AND vehicle_type = 0 AND movement = 3''', [end_date, start_date])

			d = list(qs)
			dict = {}
			for i in range(len(d)):
				dict[d[i].id_term] = d[i].value

			# Crear JSON dinamico
			content = [{"value": v, "key": k } for k, v in dict.iteritems()]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Descripcion: Circulacion de vehiculos pesados en GI Sentido O-N
# Response format: {key, value}
class WON(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		try:
			# Obtener la informacion de la BD
			if start_date == "null" or end_date == "null":
				# qs no debe incluir fechas
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE vehicle_type = 0 AND movement = 4''', [end_date, start_date])
			else:
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE date >= %s AND date <= %s AND vehicle_type = 0 AND movement = 4''', [end_date, start_date])

			d = list(qs)
			dict = {}
			for i in range(len(d)):
				dict[d[i].id_term] = d[i].value

			# Crear JSON dinamico
			content = [{"value": v, "key": k } for k, v in dict.iteritems()]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Descripcion: Circulacion de vehiculos pesados en FR Sentido O-E
# Response format: {key, value}
class WOE(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		try:
			# Obtener la informacion de la BD
			if start_date == "null" or end_date == "null":
				# qs no debe incluir fechas
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE vehicle_type = 0 AND movement = 5''', [end_date, start_date])
			else:
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE date >= %s AND date <= %s AND vehicle_type = 0 AND movement = 5''', [end_date, start_date])

			d = list(qs)
			dict = {}
			for i in range(len(d)):
				dict[d[i].id_term] = d[i].value

			# Crear JSON dinamico
			content = [{"value": v, "key": k } for k, v in dict.iteritems()]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Descripcion: Circulacion de vehiculos pesados en GI Sentido N-E
# Response format: {key, value}
class WNE(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		try:
			# Obtener la informacion de la BD
			if start_date == "null" or end_date == "null":
				# qs no debe incluir fechas
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE vehicle_type = 0 AND movement = 6''', [end_date, start_date])
			else:
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE date >= %s AND date <= %s AND vehicle_type = 0 AND movement = 6''', [end_date, start_date])

			d = list(qs)
			dict = {}
			for i in range(len(d)):
				dict[d[i].id_term] = d[i].value

			# Crear JSON dinamico
			content = [{"value": v, "key": k } for k, v in dict.iteritems()]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Grafico de barras (composicion %) para los investigadores de logistica y transporte
# Descripcion: Composicion de vehiculos pesados en GD sentido E-N
# Response format: {key, value}
class CEN(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		# Como ingresar parametros al API
		try:
			# Escoger solo en el rango de fechas determinado
			if start_date == "null" or end_date == "null":
				# qs no debe incluir fechas
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE movement = 1''');
			else:
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE date >= %s AND date <= %s AND movement = 1''', [end_date, start_date]);

			d = list(qs)

			liviano = 0
			pesado = 0

			for i in range(len(d)):
				if d[i].vehicle_type == 1:
					# Contar livianos
					liviano = liviano + d[i].value
				elif d[i].vehicle_type == 0:
					# Contar pesados
					pesado = pesado + d[i].value

			# Generar respuesta JSON
			content = [{"value":liviano, "key":"Livianos"},
				       {"value":pesado, "key":"Pesados"}
					  ]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Descripcion: Composicion de vehiculos pesados en FR Sentido E-O
# Response format: {key, value}
class CEO(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		# Como ingresar parametros al API
		try:
			# Escoger solo en el rango de fechas determinado
			if start_date == "null" or end_date == "null":
				# qs no debe incluir fechas
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE movement = 2''');
			else:
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE date >= %s AND date <= %s AND movement = 2''', [end_date, start_date]);

			d = list(qs)

			liviano = 0
			pesado = 0

			for i in range(len(d)):
				if d[i].vehicle_type == 1:
					# Contar livianos
					liviano = liviano + d[i].value
				elif d[i].vehicle_type == 0:
					# Contar pesados
					pesado = pesado + d[i].value

			# Generar respuesta JSON
			content = [{"value":liviano, "key":"Livianos"},
				       {"value":pesado, "key":"Pesados"}
					  ]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Descripcion: Composicion de vehiculos pesados en GD Sentido N-O
# Response format: {key, value}
class CNO(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		# Como ingresar parametros al API
		try:
			# Escoger solo en el rango de fechas determinado
			if start_date == "null" or end_date == "null":
				# qs no debe incluir fechas
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE movement = 3''');
			else:
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE date >= %s AND date <= %s AND movement = 3''', [end_date, start_date]);

			d = list(qs)

			liviano = 0
			pesado = 0

			for i in range(len(d)):
				if d[i].vehicle_type == 1:
					# Contar livianos
					liviano = liviano + d[i].value
				elif d[i].vehicle_type == 0:
					# Contar pesados
					pesado = pesado + d[i].value

			# Generar respuesta JSON
			content = [{"value":liviano, "key":"Livianos"},
				       {"value":pesado, "key":"Pesados"}
					  ]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Descripcion: Composicion de vehiculos pesados en GI Sentido O-N
# Response format: {key, value}
class CON(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		# Como ingresar parametros al API
		try:
			# Escoger solo en el rango de fechas determinado
			if start_date == "null" or end_date == "null":
				# qs no debe incluir fechas
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE movement = 4''');
			else:
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE date >= %s AND date <= %s AND movement = 4''', [end_date, start_date]);

			d = list(qs)

			liviano = 0
			pesado = 0

			for i in range(len(d)):
				if d[i].vehicle_type == 1:
					# Contar livianos
					liviano = liviano + d[i].value
				elif d[i].vehicle_type == 0:
					# Contar pesados
					pesado = pesado + d[i].value

			# Generar respuesta JSON
			content = [{"value":liviano, "key":"Livianos"},
				       {"value":pesado, "key":"Pesados"}
					  ]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Descripcion: Composicion de vehiculos pesados en FR Sentido O-E
# Response format: {key, value}
class COE(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		# Como ingresar parametros al API
		try:
			# Escoger solo en el rango de fechas determinado
			if start_date == "null" or end_date == "null":
				# qs no debe incluir fechas
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE movement = 5''');
			else:
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE date >= %s AND date <= %s AND movement = 5''', [end_date, start_date]);

			d = list(qs)

			liviano = 0
			pesado = 0

			for i in range(len(d)):
				if d[i].vehicle_type == 1:
					# Contar livianos
					liviano = liviano + d[i].value
				elif d[i].vehicle_type == 0:
					# Contar pesados
					pesado = pesado + d[i].value

			# Generar respuesta JSON
			content = [{"value":liviano, "key":"Livianos"},
				       {"value":pesado, "key":"Pesados"}
					  ]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Descripcion: Composicion de vehiculos pesados en GI Sentido N-E
# Response format: {key, value}
class CNE(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		# Como ingresar parametros al API
		try:
			# Escoger solo en el rango de fechas determinado
			if start_date == "null" or end_date == "null":
				# qs no debe incluir fechas
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE movement = 6''');
			else:
				qs = main_models.Logistica.objects.raw('''SELECT * FROM main_logistica WHERE date >= %s AND date <= %s AND movement = 6''', [end_date, start_date]);

			d = list(qs)

			liviano = 0
			pesado = 0

			for i in range(len(d)):
				if d[i].vehicle_type == 1:
					# Contar livianos
					liviano = liviano + d[i].value
				elif d[i].vehicle_type == 0:
					# Contar pesados
					pesado = pesado + d[i].value

			# Generar respuesta JSON
			content = [{"value":liviano, "key":"Livianos"},
				       {"value":pesado, "key":"Pesados"}
					  ]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Series de tiempo para los investigadores de cambio climatico
# Response format: {month, count}
class Minimo(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		try:
			# Obtener la informacion de la BD
			if start_date == "null" or end_date == "null":
				# qs no debe incluir fechas
				qs = main_models.Clima.objects.raw('''SELECT * FROM main_clima''')
			else:
				qs = main_models.Clima.objects.raw('''SELECT * FROM main_clima WHERE date <= %s AND date >= %s''', [end_date, start_date])
			data = list(qs)
			dict = {}
			for i in range(len(data)):
				dict[data[i].date] = data[i].tmin

			# Crear JSON dinamico
			content = [{"count": v, "month": k } for k, v in dict.iteritems()]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Response format: {month, count}
class Maximo(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		try:
			# Obtener la informacion de la BD
			if start_date == "null" or end_date == "null":
				# qs no debe incluir fechas
				qs = main_models.Clima.objects.raw('''SELECT * FROM main_clima''')
			else:
				qs = main_models.Clima.objects.raw('''SELECT * FROM main_clima WHERE date <= %s AND date >= %s''', [end_date, start_date])
			data = list(qs)
			dict = {}
			for i in range(len(data)):
				dict[data[i].date] = data[i].tmax

			# Crear JSON dinamico
			content = [{"count": v, "month": k } for k, v in dict.iteritems()]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Response format: {month, count}
class Promedio(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		try:
			# Obtener la informacion de la BD
			if start_date == "null" or end_date == "null":
				# qs no debe incluir fechas
				qs = main_models.Clima.objects.raw('''SELECT * FROM main_clima''')
			else:
				qs = main_models.Clima.objects.raw('''SELECT * FROM main_clima WHERE date <= %s AND date >= %s''', [end_date, start_date])
			data = list(qs)
			dict = {}
			for i in range(len(data)):
				dict[data[i].date] = data[i].tmean

			# Crear JSON dinamico
			content = [{"count": v, "month": k } for k, v in dict.iteritems()]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Response format: {month, count}
class RR(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		try:
			# Obtener la informacion de la BD
			if start_date == "null" or end_date == "null":
				# qs no debe incluir fechas
				qs = main_models.Clima.objects.raw('''SELECT * FROM main_clima''')
			else:
				qs = main_models.Clima.objects.raw('''SELECT * FROM main_clima WHERE date <= %s AND date >= %s''', [end_date, start_date])
			data = list(qs)
			dict = {}
			for i in range(len(data)):
				dict[data[i].date] = data[i].rr

			# Crear JSON dinamico
			content = [{"count": v, "month": k } for k, v in dict.iteritems()]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Response format: {month, count}
class ONI(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		try:
			# Obtener la informacion de la BD
			if start_date == "null" or end_date == "null":
				# qs no debe incluir fechas
				qs = main_models.Clima.objects.raw('''SELECT * FROM main_clima''')
			else:
				qs = main_models.Clima.objects.raw('''SELECT * FROM main_clima WHERE date <= %s AND date >= %s''', [end_date, start_date])
			data = list(qs)
			dict = {}
			for i in range(len(data)):
				dict[data[i].date] = data[i].oni

			# Crear JSON dinamico
			content = [{"count": v, "month": k } for k, v in dict.iteritems()]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Grafico circular para los investigadores de cambio climatico
# Response format: {key, value}
class Censo(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		# Como ingresar parametros al API
		try:
			# Escoger solo en el rango de fechas determinado
			if start_date == "null" or end_date == "null":
				# qs no debe incluir fechas
				qs = main_models.Censo.objects.raw('''SELECT * FROM main_censo''');
			else:
				qs = main_models.Censo.objects.raw('''SELECT * FROM main_censo WHERE year = %s ''', [start_date[:4]]);

			d = list(qs)

			for i in range(len(d)):
				man = d[i].man
				woman = d[i].woman

			# Generar respuesta JSON
			content = [{"value":man, "key":"Hombres"},
				       {"value":woman, "key":"Mujeres"}
					  ]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Grafico de barras para los investigadores de cambio climatico
# Response format: {key, value}
class CensoBar(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		try:
			# Obtener la informacion de la BD
			if start_date == "null" or end_date == "null":
				# qs no debe incluir fechas
				qs = main_models.Censo.objects.raw('''SELECT * FROM main_censo''');
			else:
				qs = main_models.Censo.objects.raw('''SELECT * FROM main_censo WHERE year = %s ''', [start_date[:4]]);

			d = list(qs)
			for i in range(len(d)):
				man = d[i].man
				woman = d[i].woman

			# Crear JSON dinamico
			content = [{"value": man, "key": "Hombres" },
					   {"value": woman, "key": "Mujeres" }]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

# Response format: {key, value}
class Population(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		try:
			# Obtener la informacion de la BD
			qs = main_models.Censo.objects.raw('''SELECT * FROM main_censo''');
			d = list(qs)
			dict = {}
			for i in range(len(d)):
				dict[d[i].year] = d[i].total_pob
			# Crear JSON dinamico
			content = [{"value": v, "key": k } for k, v in dict.iteritems()]

		except:
			# Si el Query retorna None
			content = {}

		return Response(content)
