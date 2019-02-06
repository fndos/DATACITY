# -*- encoding: utf-8 -*-
def metseg_a_kmhor(metseg):
	km_hora = round(3.6*float(metseg), 2)
	return km_hora

def seg_a_min(seg):
	minu=round(float(seg)/60.0,2)
	return minu

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
	AVG_EMISSION_DICT = [{"Ruido":str("{0:.2f}".format(avg[0])) + " dB"},
			   # {"value":avg[1], "key":"lane"},
			   {"CO2":str("{0:.2f}".format(avg[2])) + " mg/s"},
			   {"CO":str("{0:.2f}".format(avg[3])) + " mg/s" },
			   # {"value":avg[4], "key":"angle"},
			   # {"value":avg[5], "key":"id"},
			   # {"value":avg[6], "key":"pos"},
			   {"PMx":str("{0:.2f}".format(avg[7])) + " mg/s"},
			   # {"value":avg[8], "key":"waiting"},
			   # {"value":avg[9], "key":"electricity"},
			   {"NOx":str("{0:.2f}".format(avg[10])) + " mg/s"},
			   # {"value":avg[11], "key":"route"},
			   {"HC":str("{0:.2f}".format(avg[12])) + " mg/s"},
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
	liviano = [0] * 9
	contador_liviano=0
	contador_pesado=0
	for i in range(len(data)):
		v = data[i]['vehicle']
		if v["@type"] =="bus_bus":
			# avg[0] = avg[0] + float(v["@id"])
			avg[1] = avg[1] + float(v["@x"])
			avg[2] = avg[2] + float(v["@y"])
			avg[3] = avg[3] + float(v["@angle"])
			# avg[4] = avg[4] + float(v["@type"])
			avg[5] = avg[5] + float(v["@speed"])
			avg[6] = avg[6] + float(v["@pos"])
			# avg[7] = avg[7] + float(v["@lane"])
			avg[8] = avg[8] + float(v["@slope"])
			contador_pesado+=1
		else:
			# avg[0] = avg[0] + float(v["@id"])
			liviano[1] = liviano[1] + float(v["@x"])
			liviano[2] = liviano[2] + float(v["@y"])
			liviano[3] = liviano[3] + float(v["@angle"])
			# avg[4] = avg[4] + float(v["@type"])
			liviano[5] = liviano[5] + float(v["@speed"])
			liviano[6] = liviano[6] + float(v["@pos"])
			# avg[7] = avg[7] + float(v["@lane"])
			liviano[8] = liviano[8] + float(v["@slope"])
			contador_liviano+=1

	# Calcular el promedio
	for i in range(len(avg)):
		avg[i] = avg[i] / contador_pesado
		liviano[i] = liviano[i] / contador_liviano
	# Creo el diccionario de salida
	AVG_TRACE_DICT_PESADO = [
			   # {"value":avg[0], "key":"id"},
			   {"x":"{0:.2f}".format(avg[1])},
			   {"y":"{0:.2f}".format(avg[2])},
			   {"Angulo":"{0:.2f}".format(avg[3])},
			   # {"value":avg[4], "key":"type"},
			   {"Velocidad":str(metseg_a_kmhor(avg[5])) + " kilometros por hora"},
			   {"pos":"{0:.2f}".format(avg[6])},
			   # {"value":avg[7], "key":"lane"},
			   {"Peralte":"{0:.2f}".format(avg[8])},
			  ]
	AVG_TRACE_DICT_LIVIANO= [
			   # {"value":avg[0], "key":"id"},
			   {"x":"{0:.2f}".format(liviano[1])},
			   {"y":"{0:.2f}".format(liviano[2])},
			   {"Angulo":"{0:.2f}".format(liviano[3])},
			   # {"value":avg[4], "key":"type"},
			   {"Velocidad":str(metseg_a_kmhor(liviano[5])) + " kilometros por hora"},
			   {"pos":"{0:.2f}".format(liviano[6])},
			   # {"value":avg[7], "key":"lane"},
			   {"Peralte":"{0:.2f}".format(liviano[8])},
			  ]
	return AVG_TRACE_DICT_PESADO, AVG_TRACE_DICT_LIVIANO

def get_summary(data):
	avg = [0] * 12
	for i in range(len(data)):
		v = data[i]['step']
		avg[0] = float(v["@time"])
		avg[1] = max(avg[1], int(v["@loaded"]))
		avg[2] = max(avg[2], int(v["@inserted"]))
		avg[3] = max(avg[3], int(v["@running"]))
		avg[4] = max(avg[4], int(v["@waiting"]))
		avg[5] = int(v["@ended"])
		avg[6] = avg[6] + float(v["@meanWaitingTime"])
		avg[7] = avg[7] + float(v["@meanTravelTime"])
		avg[8] = max(avg[8], int(v["@halting"]))
		avg[9] = avg[9] + float(v["@meanSpeed"])
		avg[10] = avg[10] + float(v["@meanSpeedRelative"])
		avg[11] = avg[11] + int(v["@duration"])
	# Creo el diccionario de salida
	avg[9]=round(float(float(avg[9])/float(len(data))),2)
	avg[10]=round(float(float(avg[10])/float(len(data))),2)
	SUMMARY_DICT = [
			   {"tiempo":str(avg[0]) + " segundos"},
			   {"cargado":str(avg[1]) + " vehiculos en total"},
			   {"insertado":str(avg[2]) + " vehiculos en total"},
			   {"corriendo":str(avg[3]) + " vehiculos concurrentes"},
			   {"esperando":str(avg[4]) + " vehiculos en espera (Maximo)"},
			   {"terminado":str(avg[5]) + " vehiculos"},
			   {"tiempo de espera medio":str(seg_a_min(avg[6])) + " minutos"},
			   {"tiempo de viaje medio":str(seg_a_min(avg[7])) + " minutos"},
			   {"interrupcion":str(avg[8])+" vehiculos (Maximo)"},
			   #{"velocidad media":str(avg[9]) + " metros por segundo"},
			   {"velocidad media":str(metseg_a_kmhor(avg[9])) + " kilometros por hora"},
			   #{"velocidad relativa media":str(avg[10])  + " metros por segundo"},
			   {"velocidad relativa media":str(metseg_a_kmhor(avg[10]))  + " kilometros por hora"},
			   #{"duracion":str(avg[11]) + " segundos"},
			  ]
	return SUMMARY_DICT

# No se esta usando en esta version
def get_key_value_summary(data):
	KEY_VALUE_MEAN_SPEED_DICT = []
	KEY_VALUE_WAITING_DICT = []
	for i in range(len(data)):
		v = data[i]['step']
		KEY_VALUE_MEAN_SPEED_DICT.append({"value": v["@meanSpeed"], "key": int(float(v["@time"]))})
		KEY_VALUE_WAITING_DICT.append({"value": v["@waiting"], "key": int(float(v["@time"]))})
	return KEY_VALUE_MEAN_SPEED_DICT, KEY_VALUE_WAITING_DICT

def get_key_value_speed_by_type(data):
	WEIGHT_STEP = []
	LIGHT_STEP = []
	for x in range(len(data)):
		WEIGHT = 0
		LIGHT = 0
		TOTAL_WEIGHT = 0
		TOTAL_LIGHT = 0
		for i in range(len(data[x])):
			v = data[x][i]
			if v["@type"] == "bus_bus":
				# Vehiculo pesado
				WEIGHT = WEIGHT + float(v["@speed"])
				TOTAL_WEIGHT = TOTAL_WEIGHT + 1
			else:
				# Vehiculo liviano
				LIGHT = LIGHT + float(v["@speed"])
				TOTAL_LIGHT = TOTAL_LIGHT + 1
		# Calcular promedio
		if TOTAL_WEIGHT == 0:
			TOTAL_WEIGHT = 1
		if TOTAL_LIGHT == 0:
			TOTAL_LIGHT = 1
		WEIGHT_STEP.append("{0:.2f}".format(WEIGHT/TOTAL_WEIGHT))
		LIGHT_STEP.append("{0:.2f}".format(LIGHT/TOTAL_LIGHT))

	# Creo el diccionario de salida para vehiculos pesados
	KEY_VALUE_WEIGHT_MEAN_SPEED_DICT = []
	for i in range(len(WEIGHT_STEP)):
		KEY_VALUE_WEIGHT_MEAN_SPEED_DICT.append({"value": metseg_a_kmhor(WEIGHT_STEP[i]), "key": i})
	# Creo el diccionario de salida para vehiculos livianos
	KEY_VALUE_LIGHT_MEAN_SPEED_DICT = []
	for i in range(len(LIGHT_STEP)):
		KEY_VALUE_LIGHT_MEAN_SPEED_DICT.append({"value": metseg_a_kmhor(LIGHT_STEP[i]), "key": i})

	return KEY_VALUE_WEIGHT_MEAN_SPEED_DICT, KEY_VALUE_LIGHT_MEAN_SPEED_DICT

def get_key_value_waiting_by_type(data):
	WEIGHT_STEP = []
	LIGHT_STEP = []
	for x in range(len(data)):
		WEIGHT = 0
		LIGHT = 0
		TOTAL_WEIGHT = 0
		TOTAL_LIGHT = 0
		for i in range(len(data[x])):
			v = data[x][i]
			if v["@type"] == "bus_bus":
				# Vehiculo pesado
				WEIGHT = WEIGHT + int(float(v["@waiting"]))
				TOTAL_WEIGHT = TOTAL_WEIGHT + 1
			else:
				# Vehiculo liviano
				LIGHT = LIGHT + int(float(v["@waiting"]))
				TOTAL_LIGHT = TOTAL_LIGHT + 1
		# Calcular promedio
		if TOTAL_WEIGHT == 0:
			TOTAL_WEIGHT = 1
		if TOTAL_LIGHT == 0:
			TOTAL_LIGHT = 1
		WEIGHT_STEP.append("{0:.2f}".format(WEIGHT/TOTAL_WEIGHT))
		LIGHT_STEP.append("{0:.2f}".format(LIGHT/TOTAL_LIGHT))

	# Creo el diccionario de salida para vehiculos pesados
	KEY_VALUE_WEIGHT_WAITING_DICT = []
	for i in range(len(WEIGHT_STEP)):
		KEY_VALUE_WEIGHT_WAITING_DICT.append({"value": float(WEIGHT_STEP[i]), "key": i})
	# Creo el diccionario de salida para vehiculos livianos
	KEY_VALUE_LIGHT_WAITING_DICT = []
	for i in range(len(LIGHT_STEP)):
		KEY_VALUE_LIGHT_WAITING_DICT.append({"value": float(LIGHT_STEP[i]), "key": i})

	return KEY_VALUE_WEIGHT_WAITING_DICT, KEY_VALUE_LIGHT_WAITING_DICT
