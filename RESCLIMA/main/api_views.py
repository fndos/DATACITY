# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from timeSeries import models
from simulation import models as simulation_models
from . import serializers

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

import json

class VariableViewset(viewsets.ModelViewSet):
	queryset = models.Variable.objects.all()
	serializer_class = serializers.VariableSerializer

class StationTypeViewset(viewsets.ModelViewSet):
	queryset = models.StationType.objects.all()
	serializer_class = serializers.StationTypeSerializer

class StationViewset(viewsets.ModelViewSet):
	queryset = models.Station.objects.all()
	serializer_class = serializers.StationSerializer

# Esta clase por el momento no se esta utilizando en RESCLIMA
class ProviderViewSet(viewsets.ModelViewSet):
	queryset = models.Provider.objects.all()
	serializer_class = serializers.ProviderSerializer

class MeasurementViewSet(viewsets.ModelViewSet):
	queryset = models.Measurement.objects.all()
	serializer_class = serializers.MeasurementSerializer

class APIAverageMeasurementViewSet(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		# Obtener el diccionario para las variables
		# start_date = '2018-12-25'
		# end_date = '2018-12-27'
		qs = models.Variable.objects.all()
		dict = {}
		v = list(qs)
		for i in range(len(v)):
			dict[i] = v[i].name
		# Obtener las lecturas de las estaciones por timestamp
		try:
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

class AVGLightEmissionViewSet(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, sid=None):
		output_instance = simulation_models.Output.objects.get(simulation__id=sid)
		print output_instance.avg_light_emission[1]['CO2']
		content = {"name":"SUMO","children":[{"name":"Emission","children":[{"name":"Categoria1","children":[{"key":"CO2","value":output_instance.avg_light_emission[1]['CO2']}]},{"name":"Categoria2","children":[{"key":"CO","value":output_instance.avg_light_emission[2]['CO']}]},{"name":"Categoria3","children":[{"key":"PMx","value":output_instance.avg_light_emission[3]['PMx']}]},{"name":"Categoria4","children":[{"key":"NOx","value":output_instance.avg_light_emission[4]['NOx']}]},{"name":"Categoria5","children":[{"key":"HC","value":output_instance.avg_light_emission[5]['HC']}]}]}]}

		return Response(content)

class TreeMapViewSet(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, format=None):
		content = [
		  {
			"region": "Asia",
			"subregion": "Southern Asia",
			"value": 25500100,
			"key": "Afghanistan"
		  },
		  {
			"region": "Europe",
			"subregion": "Northern Europe",
			"value": 28502,
			"key": "Åland Islands"
		  },
		  {
			"region": "Europe",
			"subregion": "Southern Europe",
			"value": 2821977,
			"key": "Albania"
		  },
		  {
			"region": "Africa",
			"subregion": "Northern Africa",
			"value": 37900000,
			"key": "Algeria"
		  },
		  {
			"region": "Europe",
			"subregion": "Southern Europe",
			"value": 76246,
			"key": "Andorra"
		  },
		  {
			"region": "Africa",
			"subregion": "Middle Africa",
			"value": 20609294,
			"key": "Angola"
		  },
		  {
			"region": "Americas",
			"subregion": "Caribbean",
			"value": 13452,
			"key": "Anguilla"
		  },
		  {
			"region": "",
			"subregion": "",
			"value": -1,
			"key": "Antarctica"
		  },
		  {
			"region": "Americas",
			"subregion": "Caribbean",
			"value": 86295,
			"key": "Antigua and Barbuda"
		  },
		  {
			"region": "Americas",
			"subregion": "South America",
			"value": 40117096,
			"key": "Argentina"
		  },
		  {
			"region": "Asia",
			"subregion": "Western Asia",
			"value": 3024100,
			"key": "Armenia"
		  },
		  {
			"region": "Americas",
			"subregion": "Caribbean",
			"value": 101484,
			"key": "Aruba"
		  },
		  {
			"region": "Europe",
			"subregion": "Western Europe",
			"value": 8501502,
			"key": "Austria"
		  },
		  {
			"region": "Asia",
			"subregion": "Western Asia",
			"value": 9235100,
			"key": "Azerbaijan"
		  },
		  {
			"region": "Americas",
			"subregion": "Caribbean",
			"value": -1,
			"key": "Bahamas"
		  },
		  {
			"region": "Asia",
			"subregion": "Western Asia",
			"value": 1234571,
			"key": "Bahrain"
		  },
		  {
			"region": "Asia",
			"subregion": "Southern Asia",
			"value": 152518015,
			"key": "Bangladesh"
		  },
		  {
			"region": "Americas",
			"subregion": "Caribbean",
			"value": 274200,
			"key": "Barbados"
		  },
		  {
			"region": "Europe",
			"subregion": "Eastern Europe",
			"value": 9465500,
			"key": "Belarus"
		  },
		  {
			"region": "Europe",
			"subregion": "Western Europe",
			"value": 11175653,
			"key": "Belgium"
		  },
		  {
			"region": "Americas",
			"subregion": "Central America",
			"value": 312971,
			"key": "Belize"
		  },
		  {
			"region": "Africa",
			"subregion": "Western Africa",
			"value": 10323000,
			"key": "Benin"
		  },
		  {
			"region": "Americas",
			"subregion": "Northern America",
			"value": 64237,
			"key": "Bermuda"
		  },
		  {
			"region": "Asia",
			"subregion": "Southern Asia",
			"value": 740990,
			"key": "Bhutan"
		  },
		  {
			"region": "Americas",
			"subregion": "South America",
			"value": 10027254,
			"key": "Bolivia"
		  },
		  {
			"region": "Americas",
			"subregion": "Caribbean",
			"value": -1,
			"key": "Bonaire"
		  },
		  {
			"region": "Europe",
			"subregion": "Southern Europe",
			"value": 3791622,
			"key": "Bosnia and Herzegovina"
		  },
		  {
			"region": "Africa",
			"subregion": "Southern Africa",
			"value": 2024904,
			"key": "Botswana"
		  },
		  {
			"region": "",
			"subregion": "",
			"value": -1,
			"key": "Bouvet Island"
		  },
		  {
			"region": "Americas",
			"subregion": "South America",
			"value": 201032714,
			"key": "Brazil"
		  },
		  {
			"region": "Africa",
			"subregion": "Eastern Africa",
			"value": -1,
			"key": "British Indian Ocean Territory"
		  },
		  {
			"region": "Americas",
			"subregion": "Caribbean",
			"value": 29537,
			"key": "British Virgin Islands"
		  },
		  {
			"region": "Asia",
			"subregion": "South-Eastern Asia",
			"value": 393162,
			"key": "Brunei"
		  },
		  {
			"region": "Europe",
			"subregion": "Eastern Europe",
			"value": 7282041,
			"key": "Bulgaria"
		  },
		  {
			"region": "Africa",
			"subregion": "Western Africa",
			"value": 17322796,
			"key": "Burkina Faso"
		  },
		  {
			"region": "Africa",
			"subregion": "Eastern Africa",
			"value": 10163000,
			"key": "Burundi"
		  },
		  {
			"region": "Asia",
			"subregion": "South-Eastern Asia",
			"value": 15135000,
			"key": "Cambodia"
		  },
		  {
			"region": "Africa",
			"subregion": "Middle Africa",
			"value": 20386799,
			"key": "Cameroon"
		  },
		  {
			"region": "Americas",
			"subregion": "Northern America",
			"value": 35158304,
			"key": "Canada"
		  },
		  {
			"region": "Africa",
			"subregion": "Western Africa",
			"value": 491875,
			"key": "Cape Verde"
		  },
		  {
			"region": "Americas",
			"subregion": "Caribbean",
			"value": 55456,
			"key": "Cayman Islands"
		  },
		  {
			"region": "Africa",
			"subregion": "Middle Africa",
			"value": 4616000,
			"key": "Central African Republic"
		  },
		  {
			"region": "Africa",
			"subregion": "Middle Africa",
			"value": 12825000,
			"key": "Chad"
		  },
		  {
			"region": "Americas",
			"subregion": "South America",
			"value": 16634603,
			"key": "Chile"
		  },
		  {
			"region": "Asia",
			"subregion": "Eastern Asia",
			"value": 1361170000,
			"key": "China"
		  },
		  {
			"region": "Americas",
			"subregion": "South America",
			"value": 47330000,
			"key": "Colombia"
		  },
		  {
			"region": "Africa",
			"subregion": "Eastern Africa",
			"value": 724300,
			"key": "Comoros"
		  },
		  {
			"region": "Africa",
			"subregion": "Middle Africa",
			"value": 4448000,
			"key": "Republic of the Congo"
		  },
		  {
			"region": "Africa",
			"subregion": "Middle Africa",
			"value": 67514000,
			"key": "Democratic Republic of the Congo"
		  },
		  {
			"region": "Americas",
			"subregion": "Central America",
			"value": 4667096,
			"key": "Costa Rica"
		  },
		  {
			"region": "Africa",
			"subregion": "Western Africa",
			"value": -1,
			"key": "Côte d'Ivoire"
		  },
		  {
			"region": "Europe",
			"subregion": "Southern Europe",
			"value": 4290612,
			"key": "Croatia"
		  },
		  {
			"region": "Americas",
			"subregion": "Caribbean",
			"value": 11167325,
			"key": "Cuba"
		  },
		  {
			"region": "Americas",
			"subregion": "Caribbean",
			"value": 150563,
			"key": "Curaçao"
		  },
		  {
			"region": "Asia",
			"subregion": "Western Asia",
			"value": 865878,
			"key": "Cyprus"
		  },
		  {
			"region": "Europe",
			"subregion": "Eastern Europe",
			"value": 10512900,
			"key": "Czech Republic"
		  },
		  {
			"region": "Europe",
			"subregion": "Northern Europe",
			"value": 5623501,
			"key": "Denmark"
		  },
		  {
			"region": "Africa",
			"subregion": "Eastern Africa",
			"value": 864618,
			"key": "Djibouti"
		  },
		  {
			"region": "Americas",
			"subregion": "Caribbean",
			"value": 71293,
			"key": "Dominica"
		  },
		  {
			"region": "Americas",
			"subregion": "Caribbean",
			"value": 9445281,
			"key": "Dominican Republic"
		  },
		  {
			"region": "Americas",
			"subregion": "South America",
			"value": 15617900,
			"key": "Ecuador"
		  },
		  {
			"region": "Africa",
			"subregion": "Northern Africa",
			"value": 83661000,
			"key": "Egypt"
		  },
		  {
			"region": "Americas",
			"subregion": "Central America",
			"value": 6340000,
			"key": "El Salvador"
		  },
		  {
			"region": "Africa",
			"subregion": "Middle Africa",
			"value": 1622000,
			"key": "Equatorial Guinea"
		  },
		  {
			"region": "Africa",
			"subregion": "Eastern Africa",
			"value": 6333000,
			"key": "Eritrea"
		  },
		  {
			"region": "Europe",
			"subregion": "Northern Europe",
			"value": 1286540,
			"key": "Estonia"
		  },
		  {
			"region": "Africa",
			"subregion": "Eastern Africa",
			"value": 86613986,
			"key": "Ethiopia"
		  },
		  {
			"region": "Americas",
			"subregion": "South America",
			"value": 2563,
			"key": "Falkland Islands"
		  },
		  {
			"region": "Europe",
			"subregion": "Northern Europe",
			"value": 48509,
			"key": "Faroe Islands"
		  },
		  {
			"region": "Europe",
			"subregion": "Northern Europe",
			"value": 5445883,
			"key": "Finland"
		  },
		  {
			"region": "Europe",
			"subregion": "Western Europe",
			"value": 65806000,
			"key": "France"
		  },
		  {
			"region": "Americas",
			"subregion": "South America",
			"value": 229040,
			"key": "French Guiana"
		  },
		  {
			"region": "",
			"subregion": "",
			"value": -1,
			"key": "French Southern and Antarctic Lands"
		  },
		  {
			"region": "Africa",
			"subregion": "Middle Africa",
			"value": 1672000,
			"key": "Gabon"
		  },
		  {
			"region": "Africa",
			"subregion": "Western Africa",
			"value": -1,
			"key": "Gambia"
		  },
		  {
			"region": "Asia",
			"subregion": "Western Asia",
			"value": -1,
			"key": "Georgia"
		  },
		  {
			"region": "Europe",
			"subregion": "Western Europe",
			"value": 80523700,
			"key": "Germany"
		  },
		  {
			"region": "Africa",
			"subregion": "Western Africa",
			"value": 24658823,
			"key": "Ghana"
		  },
		  {
			"region": "Europe",
			"subregion": "Southern Europe",
			"value": 29752,
			"key": "Gibraltar"
		  },
		  {
			"region": "Europe",
			"subregion": "Southern Europe",
			"value": 10815197,
			"key": "Greece"
		  },
		  {
			"region": "Americas",
			"subregion": "Northern America",
			"value": 56370,
			"key": "Greenland"
		  },
		  {
			"region": "Americas",
			"subregion": "Caribbean",
			"value": 103328,
			"key": "Grenada"
		  },
		  {
			"region": "Americas",
			"subregion": "Caribbean",
			"value": 403355,
			"key": "Guadeloupe"
		  },
		  {
			"region": "Americas",
			"subregion": "Central America",
			"value": 15438384,
			"key": "Guatemala"
		  },
		  {
			"region": "Europe",
			"subregion": "Northern Europe",
			"value": 62431,
			"key": "Guernsey"
		  },
		  {
			"region": "Africa",
			"subregion": "Western Africa",
			"value": 10824200,
			"key": "Guinea"
		  },
		  {
			"region": "Africa",
			"subregion": "Western Africa",
			"value": 1704000,
			"key": "Guinea-Bissau"
		  },
		  {
			"region": "Americas",
			"subregion": "South America",
			"value": 784894,
			"key": "Guyana"
		  },
		  {
			"region": "Americas",
			"subregion": "Caribbean",
			"value": 10413211,
			"key": "Haiti"
		  },
		  {
			"region": "",
			"subregion": "",
			"value": -1,
			"key": "Heard Island and McDonald Islands"
		  },
		  {
			"region": "Europe",
			"subregion": "Southern Europe",
			"value": 800,
			"key": "Vatican City"
		  },
		  {
			"region": "Americas",
			"subregion": "Central America",
			"value": 8555072,
			"key": "Honduras"
		  },
		  {
			"region": "Asia",
			"subregion": "Eastern Asia",
			"value": 7184000,
			"key": "Hong Kong"
		  },
		  {
			"region": "Europe",
			"subregion": "Eastern Europe",
			"value": 9906000,
			"key": "Hungary"
		  },
		  {
			"region": "Europe",
			"subregion": "Northern Europe",
			"value": 325010,
			"key": "Iceland"
		  },
		  {
			"region": "Asia",
			"subregion": "Southern Asia",
			"value": 1236670000,
			"key": "India"
		  },
		  {
			"region": "Asia",
			"subregion": "South-Eastern Asia",
			"value": 237641326,
			"key": "Indonesia"
		  },
		  {
			"region": "Asia",
			"subregion": "Southern Asia",
			"value": 77068000,
			"key": "Iran"
		  },
		  {
			"region": "Asia",
			"subregion": "Western Asia",
			"value": 34035000,
			"key": "Iraq"
		  },
		  {
			"region": "Europe",
			"subregion": "Northern Europe",
			"value": -1,
			"key": "Ireland"
		  },
		  {
			"region": "Europe",
			"subregion": "Northern Europe",
			"value": 84497,
			"key": "Isle of Man"
		  },
		  {
			"region": "Asia",
			"subregion": "Western Asia",
			"value": 8092700,
			"key": "Israel"
		  },
		  {
			"region": "Europe",
			"subregion": "Southern Europe",
			"value": 59829079,
			"key": "Italy"
		  },
		  {
			"region": "Americas",
			"subregion": "Caribbean",
			"value": 2711476,
			"key": "Jamaica"
		  },
		  {
			"region": "Asia",
			"subregion": "Eastern Asia",
			"value": 127290000,
			"key": "Japan"
		  },
		  {
			"region": "Europe",
			"subregion": "Northern Europe",
			"value": 97857,
			"key": "Jersey"
		  },
		  {
			"region": "Asia",
			"subregion": "Western Asia",
			"value": 6512600,
			"key": "Jordan"
		  },
		  {
			"region": "Asia",
			"subregion": "Central Asia",
			"value": 17099000,
			"key": "Kazakhstan"
		  },
		  {
			"region": "Africa",
			"subregion": "Eastern Africa",
			"value": 44354000,
			"key": "Kenya"
		  },
		  {
			"region": "Asia",
			"subregion": "Western Asia",
			"value": 3582054,
			"key": "Kuwait"
		  },
		  {
			"region": "Asia",
			"subregion": "Central Asia",
			"value": 5551900,
			"key": "Kyrgyzstan"
		  },
		  {
			"region": "Asia",
			"subregion": "South-Eastern Asia",
			"value": 6580800,
			"key": "Laos"
		  },
		  {
			"region": "Europe",
			"subregion": "Northern Europe",
			"value": 2014000,
			"key": "Latvia"
		  },
		  {
			"region": "Asia",
			"subregion": "Western Asia",
			"value": 4822000,
			"key": "Lebanon"
		  },
		  {
			"region": "Africa",
			"subregion": "Southern Africa",
			"value": 2074000,
			"key": "Lesotho"
		  },
		  {
			"region": "Africa",
			"subregion": "Western Africa",
			"value": 4294000,
			"key": "Liberia"
		  },
		  {
			"region": "Africa",
			"subregion": "Northern Africa",
			"value": 6202000,
			"key": "Libya"
		  },
		  {
			"region": "Europe",
			"subregion": "Western Europe",
			"value": 36842,
			"key": "Liechtenstein"
		  },
		  {
			"region": "Europe",
			"subregion": "Northern Europe",
			"value": 2950684,
			"key": "Lithuania"
		  },
		  {
			"region": "Europe",
			"subregion": "Western Europe",
			"value": 537000,
			"key": "Luxembourg"
		  },
		  {
			"region": "Asia",
			"subregion": "Eastern Asia",
			"value": -1,
			"key": "Macau"
		  },
		  {
			"region": "Europe",
			"subregion": "Southern Europe",
			"value": -1,
			"key": "Macedonia"
		  },
		  {
			"region": "Africa",
			"subregion": "Eastern Africa",
			"value": 20696070,
			"key": "Madagascar"
		  },
		  {
			"region": "Africa",
			"subregion": "Eastern Africa",
			"value": 16363000,
			"key": "Malawi"
		  },
		  {
			"region": "Asia",
			"subregion": "South-Eastern Asia",
			"value": 29793600,
			"key": "Malaysia"
		  },
		  {
			"region": "Asia",
			"subregion": "Southern Asia",
			"value": 317280,
			"key": "Maldives"
		  },
		  {
			"region": "Africa",
			"subregion": "Western Africa",
			"value": 15302000,
			"key": "Mali"
		  },
		  {
			"region": "Europe",
			"subregion": "Southern Europe",
			"value": 416055,
			"key": "Malta"
		  },
		  {
			"region": "Americas",
			"subregion": "Caribbean",
			"value": 394173,
			"key": "Martinique"
		  },
		  {
			"region": "Africa",
			"subregion": "Western Africa",
			"value": 3461041,
			"key": "Mauritania"
		  },
		  {
			"region": "Africa",
			"subregion": "Eastern Africa",
			"value": 1257900,
			"key": "Mauritius"
		  },
		  {
			"region": "Africa",
			"subregion": "Eastern Africa",
			"value": 212600,
			"key": "Mayotte"
		  },
		  {
			"region": "Americas",
			"subregion": "Central America",
			"value": 118395054,
			"key": "Mexico"
		  },
		  {
			"region": "Europe",
			"subregion": "Eastern Europe",
			"value": 3559500,
			"key": "Moldova"
		  },
		  {
			"region": "Europe",
			"subregion": "Western Europe",
			"value": 36136,
			"key": "Monaco"
		  },
		  {
			"region": "Asia",
			"subregion": "Eastern Asia",
			"value": 2754685,
			"key": "Mongolia"
		  },
		  {
			"region": "Europe",
			"subregion": "Southern Europe",
			"value": 620029,
			"key": "Montenegro"
		  },
		  {
			"region": "Americas",
			"subregion": "Caribbean",
			"value": 4922,
			"key": "Montserrat"
		  },
		  {
			"region": "Africa",
			"subregion": "Northern Africa",
			"value": 33087700,
			"key": "Morocco"
		  },
		  {
			"region": "Africa",
			"subregion": "Eastern Africa",
			"value": 23700715,
			"key": "Mozambique"
		  },
		  {
			"region": "Asia",
			"subregion": "South-Eastern Asia",
			"value": -1,
			"key": "Myanmar"
		  },
		  {
			"region": "Africa",
			"subregion": "Southern Africa",
			"value": 2113077,
			"key": "Namibia"
		  },
		  {
			"region": "Asia",
			"subregion": "Southern Asia",
			"value": 26494504,
			"key": "Nepal"
		  },
		  {
			"region": "Europe",
			"subregion": "Western Europe",
			"value": 16807300,
			"key": "Netherlands"
		  },
		  {
			"region": "Americas",
			"subregion": "Central America",
			"value": 6071045,
			"key": "Nicaragua"
		  },
		  {
			"region": "Africa",
			"subregion": "Western Africa",
			"value": 17129076,
			"key": "Niger"
		  },
		  {
			"region": "Africa",
			"subregion": "Western Africa",
			"value": 173615000,
			"key": "Nigeria"
		  },
		  {
			"region": "Asia",
			"subregion": "Eastern Asia",
			"value": 24895000,
			"key": "North Korea"
		  },
		  {
			"region": "Europe",
			"subregion": "Northern Europe",
			"value": 5077798,
			"key": "Norway"
		  },
		  {
			"region": "Asia",
			"subregion": "Western Asia",
			"value": 3929000,
			"key": "Oman"
		  },
		  {
			"region": "Asia",
			"subregion": "Southern Asia",
			"value": 184845000,
			"key": "Pakistan"
		  },
		  {
			"region": "Asia",
			"subregion": "Western Asia",
			"value": -1,
			"key": "Palestine"
		  },
		  {
			"region": "Americas",
			"subregion": "Central America",
			"value": 3405813,
			"key": "Panama"
		  },
		  {
			"region": "Americas",
			"subregion": "South America",
			"value": 6783374,
			"key": "Paraguay"
		  },
		  {
			"region": "Americas",
			"subregion": "South America",
			"value": 30475144,
			"key": "Peru"
		  },
		  {
			"region": "Asia",
			"subregion": "South-Eastern Asia",
			"value": 98678000,
			"key": "Philippines"
		  },
		  {
			"region": "Europe",
			"subregion": "Eastern Europe",
			"value": 38533299,
			"key": "Poland"
		  },
		  {
			"region": "Europe",
			"subregion": "Southern Europe",
			"value": 10562178,
			"key": "Portugal"
		  },
		  {
			"region": "Americas",
			"subregion": "Caribbean",
			"value": 3667084,
			"key": "Puerto Rico"
		  },
		  {
			"region": "Asia",
			"subregion": "Western Asia",
			"value": 2024707,
			"key": "Qatar"
		  },
		  {
			"region": "Europe",
			"subregion": "Eastern Europe",
			"value": 1733842,
			"key": "Republic of Kosovo"
		  },
		  {
			"region": "Africa",
			"subregion": "Eastern Africa",
			"value": 821136,
			"key": "Réunion"
		  },
		  {
			"region": "Europe",
			"subregion": "Eastern Europe",
			"value": 20121641,
			"key": "Romania"
		  },
		  {
			"region": "Europe",
			"subregion": "Eastern Europe",
			"value": 143500000,
			"key": "Russia"
		  },
		  {
			"region": "Africa",
			"subregion": "Eastern Africa",
			"value": 10537222,
			"key": "Rwanda"
		  },
		  {
			"region": "Americas",
			"subregion": "Caribbean",
			"value": 8938,
			"key": "Saint Barthélemy"
		  },
		  {
			"region": "Africa",
			"subregion": "Western Africa",
			"value": -1,
			"key": "Saint Helena"
		  },
		  {
			"region": "Americas",
			"subregion": "Caribbean",
			"value": 54000,
			"key": "Saint Kitts and Nevis"
		  },
		  {
			"region": "Americas",
			"subregion": "Caribbean",
			"value": 166526,
			"key": "Saint Lucia"
		  },
		  {
			"region": "Americas",
			"subregion": "Caribbean",
			"value": -1,
			"key": "Saint Martin"
		  },
		  {
			"region": "Americas",
			"subregion": "Northern America",
			"value": 6081,
			"key": "Saint Pierre and Miquelon"
		  },
		  {
			"region": "Americas",
			"subregion": "Caribbean",
			"value": 109000,
			"key": "Saint Vincent and the Grenadines"
		  },
		  {
			"region": "Europe",
			"subregion": "Southern Europe",
			"value": 32509,
			"key": "San Marino"
		  },
		  {
			"region": "Africa",
			"subregion": "Middle Africa",
			"value": 187356,
			"key": "São Tomé and Príncipe"
		  },
		  {
			"region": "Asia",
			"subregion": "Western Asia",
			"value": 29994272,
			"key": "Saudi Arabia"
		  },
		  {
			"region": "Africa",
			"subregion": "Western Africa",
			"value": 13567338,
			"key": "Senegal"
		  },
		  {
			"region": "Europe",
			"subregion": "Southern Europe",
			"value": 7181505,
			"key": "Serbia"
		  },
		  {
			"region": "Africa",
			"subregion": "Eastern Africa",
			"value": 90945,
			"key": "Seychelles"
		  },
		  {
			"region": "Africa",
			"subregion": "Western Africa",
			"value": 6190280,
			"key": "Sierra Leone"
		  },
		  {
			"region": "Asia",
			"subregion": "South-Eastern Asia",
			"value": 5399200,
			"key": "Singapore"
		  },
		  {
			"region": "Americas",
			"subregion": "Caribbean",
			"value": 37429,
			"key": "Sint Maarten"
		  },
		  {
			"region": "Europe",
			"subregion": "Eastern Europe",
			"value": 5412008,
			"key": "Slovakia"
		  },
		  {
			"region": "Europe",
			"subregion": "Southern Europe",
			"value": 2061405,
			"key": "Slovenia"
		  },
		  {
			"region": "Africa",
			"subregion": "Eastern Africa",
			"value": 10496000,
			"key": "Somalia"
		  },
		  {
			"region": "Africa",
			"subregion": "Southern Africa",
			"value": 52981991,
			"key": "South Africa"
		  },
		  {
			"region": "Americas",
			"subregion": "South America",
			"value": -1,
			"key": "South Georgia"
		  },
		  {
			"region": "Asia",
			"subregion": "Eastern Asia",
			"value": 50219669,
			"key": "South Korea"
		  },
		  {
			"region": "Africa",
			"subregion": "Middle Africa",
			"value": 11296000,
			"key": "South Sudan"
		  },
		  {
			"region": "Europe",
			"subregion": "Southern Europe",
			"value": 46704314,
			"key": "Spain"
		  },
		  {
			"region": "Asia",
			"subregion": "Southern Asia",
			"value": 20277597,
			"key": "Sri Lanka"
		  },
		  {
			"region": "Africa",
			"subregion": "Northern Africa",
			"value": 37964000,
			"key": "Sudan"
		  },
		  {
			"region": "Americas",
			"subregion": "South America",
			"value": 534189,
			"key": "Suriname"
		  },
		  {
			"region": "Europe",
			"subregion": "Northern Europe",
			"value": 2655,
			"key": "Svalbard and Jan Mayen"
		  },
		  {
			"region": "Africa",
			"subregion": "Southern Africa",
			"value": 1250000,
			"key": "Swaziland"
		  },
		  {
			"region": "Europe",
			"subregion": "Northern Europe",
			"value": 9625444,
			"key": "Sweden"
		  },
		  {
			"region": "Europe",
			"subregion": "Western Europe",
			"value": 8085300,
			"key": "Switzerland"
		  },
		  {
			"region": "Asia",
			"subregion": "Western Asia",
			"value": 21898000,
			"key": "Syria"
		  },
		  {
			"region": "Asia",
			"subregion": "Eastern Asia",
			"value": 23361147,
			"key": "Taiwan"
		  },
		  {
			"region": "Asia",
			"subregion": "Central Asia",
			"value": 8000000,
			"key": "Tajikistan"
		  },
		  {
			"region": "Africa",
			"subregion": "Eastern Africa",
			"value": 44928923,
			"key": "Tanzania"
		  },
		  {
			"region": "Asia",
			"subregion": "South-Eastern Asia",
			"value": 65926261,
			"key": "Thailand"
		  },
		  {
			"region": "Asia",
			"subregion": "South-Eastern Asia",
			"value": -1,
			"key": "Timor-Leste"
		  },
		  {
			"region": "Africa",
			"subregion": "Western Africa",
			"value": 6191155,
			"key": "Togo"
		  },
		  {
			"region": "Americas",
			"subregion": "Caribbean",
			"value": 1328019,
			"key": "Trinidad and Tobago"
		  },
		  {
			"region": "Africa",
			"subregion": "Northern Africa",
			"value": 10833431,
			"key": "Tunisia"
		  },
		  {
			"region": "Asia",
			"subregion": "Western Asia",
			"value": 75627384,
			"key": "Turkey"
		  },
		  {
			"region": "Asia",
			"subregion": "Central Asia",
			"value": 5240000,
			"key": "Turkmenistan"
		  },
		  {
			"region": "Americas",
			"subregion": "Caribbean",
			"value": 31458,
			"key": "Turks and Caicos Islands"
		  },
		  {
			"region": "Africa",
			"subregion": "Eastern Africa",
			"value": 35357000,
			"key": "Uganda"
		  },
		  {
			"region": "Europe",
			"subregion": "Eastern Europe",
			"value": 45461627,
			"key": "Ukraine"
		  },
		  {
			"region": "Asia",
			"subregion": "Western Asia",
			"value": 8264070,
			"key": "United Arab Emirates"
		  },
		  {
			"region": "Europe",
			"subregion": "Northern Europe",
			"value": 63705000,
			"key": "United Kingdom"
		  },
		  {
			"region": "Americas",
			"subregion": "Northern America",
			"value": 317101000,
			"key": "United States"
		  },
		  {
			"region": "Americas",
			"subregion": "Northern America",
			"value": -1,
			"key": "United States Minor Outlying Islands"
		  },
		  {
			"region": "Americas",
			"subregion": "Caribbean",
			"value": 106405,
			"key": "United States Virgin Islands"
		  },
		  {
			"region": "Americas",
			"subregion": "South America",
			"value": 3286314,
			"key": "Uruguay"
		  },
		  {
			"region": "Asia",
			"subregion": "Central Asia",
			"value": 30183400,
			"key": "Uzbekistan"
		  },
		  {
			"region": "Americas",
			"subregion": "South America",
			"value": 28946101,
			"key": "Venezuela"
		  },
		  {
			"region": "Asia",
			"subregion": "South-Eastern Asia",
			"value": 90388000,
			"key": "Vietnam"
		  },
		  {
			"region": "Africa",
			"subregion": "Northern Africa",
			"value": 567000,
			"key": "Western Sahara"
		  },
		  {
			"region": "Asia",
			"subregion": "Western Asia",
			"value": 24527000,
			"key": "Yemen"
		  },
		  {
			"region": "Africa",
			"subregion": "Eastern Africa",
			"value": 13092666,
			"key": "Zambia"
		  },
		  {
			"region": "Africa",
			"subregion": "Eastern Africa",
			"value": 12973808,
			"key": "Zimbabwe"
		  }
		]

		return Response(content)

class APILightONViewSet(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		try:
			# Obtener la informacion de la BD
			qs = simulation_models.Vehicle.objects.raw('''SELECT * FROM simulation_vehicle as v INNER JOIN simulation_term as t ON v.term_id = t.id INNER JOIN simulation_gauging as g ON t.gauging_id = g.id WHERE g.date <= %s AND g.date >= %s AND v.type = 1 AND v.movement = 1''', [end_date, start_date]);
			qt = simulation_models.Term.objects.raw('''SELECT * FROM simulation_term as t INNER JOIN simulation_vehicle as v ON v.term_id = t.id INNER JOIN simulation_gauging as g ON t.gauging_id = g.id WHERE g.date <= %s AND g.date >= %s AND v.type = 1 AND v.movement = 1''', [end_date, start_date]);
			d = list(qs)
			t = list(qt)

			dict = {}
			for i in range(len(d)):
				dict[t[i].number] = d[i].number

			# Crear JSON dinamico
			content = [{"value": v, "key": k } for k, v in dict.iteritems()]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

class APILightOEViewSet(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		try:
			# Obtener la informacion de la BD
			qs = simulation_models.Vehicle.objects.raw('''SELECT * FROM simulation_vehicle as v INNER JOIN simulation_term as t ON v.term_id = t.id INNER JOIN simulation_gauging as g ON t.gauging_id = g.id WHERE g.date <= %s AND g.date >= %s AND v.type = 1 AND v.movement = 2''', [end_date, start_date]);
			qt = simulation_models.Term.objects.raw('''SELECT * FROM simulation_term as t INNER JOIN simulation_vehicle as v ON v.term_id = t.id INNER JOIN simulation_gauging as g ON t.gauging_id = g.id WHERE g.date <= %s AND g.date >= %s AND v.type = 1 AND v.movement = 2''', [end_date, start_date]);
			d = list(qs)
			t = list(qt)

			dict = {}
			for i in range(len(d)):
				dict[t[i].number] = d[i].number

			# Crear JSON dinamico
			content = [{"value": v, "key": k } for k, v in dict.iteritems()]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

class APILightNEViewSet(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		try:
			# Obtener la informacion de la BD
			qs = simulation_models.Vehicle.objects.raw('''SELECT * FROM simulation_vehicle as v INNER JOIN simulation_term as t ON v.term_id = t.id INNER JOIN simulation_gauging as g ON t.gauging_id = g.id WHERE g.date <= %s AND g.date >= %s AND v.type = 1 AND v.movement = 3''', [end_date, start_date]);
			qt = simulation_models.Term.objects.raw('''SELECT * FROM simulation_term as t INNER JOIN simulation_vehicle as v ON v.term_id = t.id INNER JOIN simulation_gauging as g ON t.gauging_id = g.id WHERE g.date <= %s AND g.date >= %s AND v.type = 1 AND v.movement = 3''', [end_date, start_date]);
			d = list(qs)
			t = list(qt)

			dict = {}
			for i in range(len(d)):
				dict[t[i].number] = d[i].number

			# Crear JSON dinamico
			content = [{"value": v, "key": k } for k, v in dict.iteritems()]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

class APIWeightONViewSet(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		try:
			# Obtener la informacion de la BD
			qs = simulation_models.Vehicle.objects.raw('''SELECT * FROM simulation_vehicle as v INNER JOIN simulation_term as t ON v.term_id = t.id INNER JOIN simulation_gauging as g ON t.gauging_id = g.id WHERE g.date <= %s AND g.date >= %s AND v.type = 2 AND v.movement = 1''', [end_date, start_date]);
			qt = simulation_models.Term.objects.raw('''SELECT * FROM simulation_term as t INNER JOIN simulation_vehicle as v ON v.term_id = t.id INNER JOIN simulation_gauging as g ON t.gauging_id = g.id WHERE g.date <= %s AND g.date >= %s AND v.type = 2 AND v.movement = 1''', [end_date, start_date]);
			d = list(qs)
			t = list(qt)

			dict = {}
			for i in range(len(d)):
				dict[t[i].number] = d[i].number

			# Crear JSON dinamico
			content = [{"value": v, "key": k } for k, v in dict.iteritems()]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

class APIWeightOEViewSet(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		try:
			# Obtener la informacion de la BD
			qs = simulation_models.Vehicle.objects.raw('''SELECT * FROM simulation_vehicle as v INNER JOIN simulation_term as t ON v.term_id = t.id INNER JOIN simulation_gauging as g ON t.gauging_id = g.id WHERE g.date <= %s AND g.date >= %s AND v.type = 2 AND v.movement = 2''', [end_date, start_date]);
			qt = simulation_models.Term.objects.raw('''SELECT * FROM simulation_term as t INNER JOIN simulation_vehicle as v ON v.term_id = t.id INNER JOIN simulation_gauging as g ON t.gauging_id = g.id WHERE g.date <= %s AND g.date >= %s AND v.type = 2 AND v.movement = 2''', [end_date, start_date]);
			d = list(qs)
			t = list(qt)

			dict = {}
			for i in range(len(d)):
				dict[t[i].number] = d[i].number

			# Crear JSON dinamico
			content = [{"value": v, "key": k } for k, v in dict.iteritems()]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

class APIWeightNEViewSet(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, start_date=None, end_date=None):
		try:
			# Obtener la informacion de la BD
			qs = simulation_models.Vehicle.objects.raw('''SELECT * FROM simulation_vehicle as v INNER JOIN simulation_term as t ON v.term_id = t.id INNER JOIN simulation_gauging as g ON t.gauging_id = g.id WHERE g.date <= %s AND g.date >= %s AND v.type = 2 AND v.movement = 3''', [end_date, start_date]);
			qt = simulation_models.Term.objects.raw('''SELECT * FROM simulation_term as t INNER JOIN simulation_vehicle as v ON v.term_id = t.id INNER JOIN simulation_gauging as g ON t.gauging_id = g.id WHERE g.date <= %s AND g.date >= %s AND v.type = 2 AND v.movement = 3''', [end_date, start_date]);
			d = list(qs)
			t = list(qt)

			dict = {}
			for i in range(len(d)):
				dict[t[i].number] = d[i].number

			# Crear JSON dinamico
			content = [{"value": v, "key": k } for k, v in dict.iteritems()]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

class APICompositionONViewSet(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, date=None):
		# Como ingresar parametros al API
		try:
			# Escoger solo en el rango de fechas determinado
			qs = simulation_models.Vehicle.objects.raw('''SELECT * FROM simulation_vehicle as v INNER JOIN simulation_term as t ON v.term_id = t.id INNER JOIN simulation_gauging as g ON t.gauging_id = g.id WHERE g.date = %s AND v.movement = 1''', [date]);
			d = list(qs)

			print len(d)

			liviano = 0
			pesado = 0
			total = 0

			for i in range(len(d)):
				if d[i].type == 1:
					# Contar livianos
					liviano = liviano + d[i].number
				elif d[i].type == 2:
					# Contar pesados
					pesado = pesado + d[i].number
				# Contar todos
				total = total + d[i].number

			# Calcular equivalente porcentual
			sum_liviano = (liviano * 100) / total
			sum_pesado = (pesado * 100) / total

			# Generar respuesta JSON
			content = [{"data": liviano, "value":sum_liviano, "key":"Livianos"},
				       {"data": pesado, "value":sum_pesado, "key":"Pesados"}
					  ]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

class APICompositionOEViewSet(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, date=None):
		# Como ingresar parametros al API
		try:
			# Escoger solo en el rango de fechas determinado
			qs = simulation_models.Vehicle.objects.raw('''SELECT * FROM simulation_vehicle as v INNER JOIN simulation_term as t ON v.term_id = t.id INNER JOIN simulation_gauging as g ON t.gauging_id = g.id WHERE g.date = %s AND v.movement = 2''', [date]);
			d = list(qs)

			print len(d)

			liviano = 0
			pesado = 0
			total = 0

			for i in range(len(d)):
				if d[i].type == 1:
					# Contar livianos
					liviano = liviano + d[i].number
				elif d[i].type == 2:
					# Contar pesados
					pesado = pesado + d[i].number
				# Contar todos
				total = total + d[i].number

			# Calcular equivalente porcentual
			sum_liviano = (liviano * 100) / total
			sum_pesado = (pesado * 100) / total

			# Generar respuesta JSON
			content = [{"data": liviano, "value":sum_liviano, "key":"Livianos"},
				       {"data": pesado, "value":sum_pesado, "key":"Pesados"}
					  ]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

class APICompositionNEViewSet(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, date=None):
		# Como ingresar parametros al API
		try:
			# Escoger solo en el rango de fechas determinado
			qs = simulation_models.Vehicle.objects.raw('''SELECT * FROM simulation_vehicle as v INNER JOIN simulation_term as t ON v.term_id = t.id INNER JOIN simulation_gauging as g ON t.gauging_id = g.id WHERE g.date = %s AND v.movement = 3''', [date]);
			d = list(qs)

			print len(d)

			liviano = 0
			pesado = 0
			total = 0

			for i in range(len(d)):
				if d[i].type == 1:
					# Contar livianos
					liviano = liviano + d[i].number
				elif d[i].type == 2:
					# Contar pesados
					pesado = pesado + d[i].number
				# Contar todos
				total = total + d[i].number

			# Calcular equivalente porcentual
			sum_liviano = (liviano * 100) / total
			sum_pesado = (pesado * 100) / total

			# Generar respuesta JSON
			content = [{"data": liviano, "value":sum_liviano, "key":"Livianos"},
				       {"data": pesado, "value":sum_pesado, "key":"Pesados"}
					  ]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)

class APICompositionViewSet(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, date=None):
		# Como ingresar parametros al API
		try:
			# Escoger solo en el rango de fechas determinado
			qs = simulation_models.Vehicle.objects.raw('''SELECT * FROM simulation_vehicle as v INNER JOIN simulation_term as t ON v.term_id = t.id INNER JOIN simulation_gauging as g ON t.gauging_id = g.id WHERE g.date = %s''', [date]);
			d = list(qs)

			print len(d)

			liviano = 0
			pesado = 0
			total = 0

			for i in range(len(d)):
				if d[i].type == 1:
					# Contar livianos
					liviano = liviano + d[i].number
				elif d[i].type == 2:
					# Contar pesados
					pesado = pesado + d[i].number
				# Contar todos
				total = total + d[i].number

			# Calcular equivalente porcentual
			sum_liviano = (liviano * 100) / total
			sum_pesado = (pesado * 100) / total

			# Generar respuesta JSON
			content = [{"data": liviano, "value":sum_liviano, "key":"Livianos"},
				       {"data": pesado, "value":sum_pesado, "key":"Pesados"}
					  ]
		except:
			# Si el Query retorna None
			content = {}

		return Response(content)
