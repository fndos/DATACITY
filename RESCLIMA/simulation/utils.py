# -*- encoding: utf-8 -*-

def cutter(path):
	temp = path
	cut_position = 0
	for i in range(len(temp)-1):
		if temp[i] == "/":
			cut_position = cut_position + 1
			if cut_position == 4:
				cut_position = i
			if cut_position == 3:
				cut_user = i
	return temp, cut_position, cut_user

def get_average_emission(data):
	avg = [0] * 19
	for i in range(len(data)):
		v = data[i]['vehicle']
		avg[0] = avg[0] + float(v["@noise"])
		# avg[1] = avg[1] + v["@lane"]
		avg[2] = avg[2] + float(v["@CO2"])
		avg[3] = avg[3] + float(v["@CO"])
		avg[4] = avg[4] + float(v["@angle"])
		# avg[5] = avg[5] + v["@id"]
		avg[6] = avg[6] + float(v["@pos"])
		avg[7] = avg[7] + float(v["@PMx"])
		avg[8] = avg[8] + float(v["@waiting"])
		avg[9] = avg[9] + float(v["@electricity"])
		avg[10] = avg[10] + float(v["@NOx"])
		# avg[11] = avg[11] + v["@route"]
		avg[12] = avg[12] + float(v["@HC"])
		avg[13] = avg[13] + float(v["@fuel"])
		avg[14] = avg[14] + float(v["@x"])
		avg[15] = avg[15] + float(v["@y"])
		# avg[16] = avg[16] + v["@eclass"]
		# avg[17] = avg[17] + v["@type"]
		avg[18] = avg[18] + float(v["@speed"])
	# Calcular el promedio
	for i in range(len(avg)):
		avg[i] = avg[i] / len(data)
	# Creo el diccionario de salida
	AVG_EMISSION_DICT = [{"noise":avg[0]},
			   # {"value":avg[1], "key":"lane"},
			   {"CO2":avg[2]},
			   {"CO":avg[3]},
			   # {"value":avg[4], "key":"angle"},
			   # {"value":avg[5], "key":"id"},
			   # {"value":avg[6], "key":"pos"},
			   {"PMx":avg[7]},
			   # {"value":avg[8], "key":"waiting"},
			   # {"value":avg[9], "key":"electricity"},
			   {"NOx":avg[10]},
			   # {"value":avg[11], "key":"route"},
			   {"HC":avg[12]},
			   # {"value":avg[13], "key":"fuel"},
			   # {"value":avg[14], "key":"x"},
			   # {"value":avg[15], "key":"y"},
			   # {"value":avg[16], "key":"eclass"},
			   # {"value":avg[17], "key":"type"},
			   # {"value":avg[18], "key":"speed"},
			  ]
	return AVG_EMISSION_DICT

def get_average_emission_by_type(data):
	avg = [0] * 19
	sum = [0] * 19
	for i in range(len(data)):
		v = data[i]['vehicle']
		if v["@type"] == "bus_bus":
			# Vehiculo Pesado
			avg[0] = avg[0] + float(v["@noise"])
			# avg[1] = avg[1] + v["@lane"]
			avg[2] = avg[2] + float(v["@CO2"])
			avg[3] = avg[3] + float(v["@CO"])
			avg[4] = avg[4] + float(v["@angle"])
			# avg[5] = avg[5] + v["@id"]
			avg[6] = avg[6] + float(v["@pos"])
			avg[7] = avg[7] + float(v["@PMx"])
			avg[8] = avg[8] + float(v["@waiting"])
			avg[9] = avg[9] + float(v["@electricity"])
			avg[10] = avg[10] + float(v["@NOx"])
			# avg[11] = avg[11] + v["@route"]
			avg[12] = avg[12] + float(v["@HC"])
			avg[13] = avg[13] + float(v["@fuel"])
			avg[14] = avg[14] + float(v["@x"])
			avg[15] = avg[15] + float(v["@y"])
			# avg[16] = avg[16] + v["@eclass"]
			# avg[17] = avg[17] + v["@type"]
			avg[18] = avg[18] + float(v["@speed"])
		else:
			# Vehiculo Liviano
			sum[0] = sum[0] + float(v["@noise"])
			# sum[1] = sum[1] + v["@lane"]
			sum[2] = sum[2] + float(v["@CO2"])
			sum[3] = sum[3] + float(v["@CO"])
			sum[4] = sum[4] + float(v["@angle"])
			# sum[5] = sum[5] + v["@id"]
			sum[6] = sum[6] + float(v["@pos"])
			sum[7] = sum[7] + float(v["@PMx"])
			sum[8] = sum[8] + float(v["@waiting"])
			sum[9] = sum[9] + float(v["@electricity"])
			sum[10] = sum[10] + float(v["@NOx"])
			# sum[11] = sum[11] + v["@route"]
			sum[12] = sum[12] + float(v["@HC"])
			sum[13] = sum[13] + float(v["@fuel"])
			sum[14] = sum[14] + float(v["@x"])
			sum[15] = sum[15] + float(v["@y"])
			# sum[16] = sum[16] + v["@eclass"]
			# sum[17] = sum[17] + v["@type"]
			sum[18] = sum[18] + float(v["@speed"])

	# Calcular el promedio de vehiculos pesados
	for i in range(len(avg)):
		avg[i] = avg[i] / len(data)
	# Calcular el promedio de vehiculos livianos
	for i in range(len(sum)):
		sum[i] = sum[i] / len(data)
	# Creo el diccionario de salida para vehiculos pesados
	AVG_WEIGHT_EMISSION_DICT = [{"noise":avg[0]},
			   # {"value":avg[1], "key":"lane"},
			   {"CO2":avg[2]},
			   {"CO":avg[3]},
			   # {"value":avg[4], "key":"angle"},
			   # {"value":avg[5], "key":"id"},
			   # {"value":avg[6], "key":"pos"},
			   {"PMx":avg[7]},
			   # {"value":avg[8], "key":"waiting"},
			   # {"value":avg[9], "key":"electricity"},
			   {"NOx":avg[10]},
			   # {"value":avg[11], "key":"route"},
			   {"HC":avg[12]},
			   # {"value":avg[13], "key":"fuel"},
			   # {"value":avg[14], "key":"x"},
			   # {"value":avg[15], "key":"y"},
			   # {"value":avg[16], "key":"eclass"},
			   # {"value":avg[17], "key":"type"},
			   # {"value":avg[18], "key":"speed"},
			  ]
	# Creo el diccionario de salida para vehiculos livianos
	AVG_LIGHT_EMISSION_DICT = [{"noise":sum[0]},
	       # {"value":sum[1], "key":"lane"},
	       {"CO2":sum[2]},
	       {"CO":sum[3]},
	       # {"value":sum[4], "key":"angle"},
	       # {"value":sum[5], "key":"id"},
	       # {"value":sum[6], "key":"pos"},
	       {"PMx":sum[7]},
	       # {"value":sum[8], "key":"waiting"},
	       # {"value":sum[9], "key":"electricity"},
	       {"NOx":sum[10]},
	       # {"value":sum[11], "key":"route"},
	       {"HC":sum[12]},
	       # {"value":sum[13], "key":"fuel"},
	       # {"value":sum[14], "key":"x"},
	       # {"value":sum[15], "key":"y"},
	       # {"value":sum[16], "key":"eclass"},
	       # {"value":sum[17], "key":"type"},
	       # {"value":sum[18], "key":"speed"},
	      ]
	return AVG_WEIGHT_EMISSION_DICT, AVG_LIGHT_EMISSION_DICT

def get_average_trace(data):
	avg = [0] * 9
	for i in range(len(data)):
		v = data[i]['vehicle']
		# avg[0] = avg[0] + float(v["@id"])
		avg[1] = avg[1] + float(v["@x"])
		avg[2] = avg[2] + float(v["@y"])
		avg[3] = avg[3] + float(v["@angle"])
		# avg[4] = avg[4] + float(v["@type"])
		avg[5] = avg[5] + float(v["@speed"])
		avg[6] = avg[6] + float(v["@pos"])
		# avg[7] = avg[7] + float(v["@lane"])
		avg[8] = avg[8] + float(v["@slope"])
	# Calcular el promedio
	for i in range(len(avg)):
		avg[i] = avg[i] / len(data)
	# Creo el diccionario de salida
	AVG_TRACE_DICT = [
			   # {"value":avg[0], "key":"id"},
			   {"x":avg[1]},
			   {"y":avg[2]},
			   {"angle":avg[3]},
			   # {"value":avg[4], "key":"type"},
			   {"speed":avg[5]},
			   {"pos":avg[6]},
			   # {"value":avg[7], "key":"lane"},
			   {"slope":avg[8]},
			  ]
	return AVG_TRACE_DICT

def get_average_trace_by_type(data):
	avg = [0] * 9
	sum = [0] * 9
	for i in range(len(data)):
		v = data[i]['vehicle']
		if v["@type"] == "bus_bus":
			# Vehiculo Pesado
			# avg[0] = avg[0] + float(v["@id"])
			avg[1] = avg[1] + float(v["@x"])
			avg[2] = avg[2] + float(v["@y"])
			avg[3] = avg[3] + float(v["@angle"])
			# avg[4] = avg[4] + float(v["@type"])
			avg[5] = avg[5] + float(v["@speed"])
			avg[6] = avg[6] + float(v["@pos"])
			# avg[7] = avg[7] + float(v["@lane"])
			avg[8] = avg[8] + float(v["@slope"])
		else:
			# Vehiculo Liviano
			# sum[0] = sum[0] + float(v["@id"])
			sum[1] = sum[1] + float(v["@x"])
			sum[2] = sum[2] + float(v["@y"])
			sum[3] = sum[3] + float(v["@angle"])
			# sum[4] = sum[4] + float(v["@type"])
			sum[5] = sum[5] + float(v["@speed"])
			sum[6] = sum[6] + float(v["@pos"])
			# sum[7] = sum[7] + float(v["@lane"])
			sum[8] = sum[8] + float(v["@slope"])

	# Calcular el promedio de vehiculos pesados
	for i in range(len(avg)):
		avg[i] = avg[i] / len(data)
	# Calcular el promedio de vehiculos livianos
	for i in range(len(sum)):
		sum[i] = sum[i] / len(data)
	# Creo el diccionario de salida para vehiculos pesados
	AVG_WEIGHT_TRACE_DICT = [
			   # {"value":avg[0], "key":"id"},
			   {"x":avg[1]},
			   {"y":avg[2]},
			   {"angle":avg[3]},
			   # {"value":avg[4], "key":"type"},
			   {"speed":avg[5]},
			   {"pos":avg[6]},
			   # {"value":avg[7], "key":"lane"},
			   {"slope":avg[8]},
			  ]
	# Creo el diccionario de salida para vehiculos livianos
	AVG_LIGHT_TRACE_DICT = [
	       # {"value":sum[0], "key":"id"},
		    {"x":sum[1]},
		    {"y":sum[2]},
		    {"angle":sum[3]},
		    # {"value":sum[4], "key":"type"},
		    {"speed":sum[5]},
		    {"pos":sum[6]},
		    # {"value":sum[7], "key":"lane"},
		    {"slope":sum[8]},
	      ]
	return AVG_WEIGHT_TRACE_DICT, AVG_LIGHT_TRACE_DICT

def get_summary(data):
	avg = [0] * 12
	for i in range(len(data)):
		v = data[i]['step']
		avg[0] = avg[0] + float(v["@time"])
		avg[1] = avg[1] + int(v["@loaded"])
		avg[2] = avg[2] + int(v["@inserted"])
		avg[3] = avg[3] + int(v["@running"])
		avg[4] = avg[4] + int(v["@waiting"])
		avg[5] = avg[5] + int(v["@ended"])
		avg[6] = avg[6] + float(v["@meanWaitingTime"])
		avg[7] = avg[7] + float(v["@meanTravelTime"])
		avg[8] = avg[8] + int(v["@halting"])
		avg[9] = avg[9] + float(v["@meanSpeed"])
		avg[10] = avg[10] + float(v["@meanSpeedRelative"])
		avg[11] = avg[11] + int(v["@duration"])
	# Creo el diccionario de salida
	SUMMARY_DICT = [
			   {"time":avg[0]},
			   {"loaded":avg[1]},
			   {"inserted":avg[2]},
			   {"running":avg[3]},
			   {"waiting":avg[4]},
			   {"ended":avg[5]},
			   {"meanWaitingTime":avg[6]},
			   {"meanTravelTime":avg[7]},
			   {"halting":avg[8]},
			   {"meanSpeed":avg[9]},
			   {"meanSpeedRelative":avg[10]},
			   {"duration":avg[11]},
			  ]
	return SUMMARY_DICT
