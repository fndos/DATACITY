# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

from celery import shared_task
from celery_progress.backend import ProgressRecorder

import time

import os, sys, errno
import subprocess
import shutil

from django.conf import settings

@shared_task(bind=True)
def simulation_task(self, params):
	# PATH sumocfg, Step de la simulacion
	progress_recorder = ProgressRecorder(self)

	try:
		#os.environ["SUMO_HOME"] = "/home/fernando/sumo-git"
		os.environ["SUMO_HOME"] = "/home/carlos/sumo-1.1.0/sumo"
		tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
		sys.path.append(tools)
		import sumolib
		import traci
		MEDIA = settings.MEDIA_ROOT
		try:
		  os.mkdir(os.path.join(MEDIA + params['simulation_path'], 'output'))
		except OSError as e:
		  if e.errno != errno.EEXIST:
			  raise
		PATH = MEDIA + params['simulation_whole_path']
		# Definiendo las salidas de la simulacion
		TRACE_OUT = MEDIA + params['simulation_path'] + "output/resclima_trace_output.xml"
		EMISSION_OUT = MEDIA + params['simulation_path'] + "output/resclima_emission_output.xml"
		SUMMARY_OUT = MEDIA + params['simulation_path'] + "output/resclima_summary_output.xml"
		# Definiendo la ruta del simulador y realizar la simulacion
		#sumoBinary = "/home/fernando/sumo-git/bin/sumo"
		sumoBinary = "/home/carlos/sumo-1.1.0/sumo/bin/sumo"
		sumoCmd = [sumoBinary, "-c", PATH, "--fcd-output", TRACE_OUT, "--emission-output", EMISSION_OUT, "--summary", SUMMARY_OUT]
		traci.start(sumoCmd, port=8888)
		print("Realizando la simulacion...")
		step = 0
		while step < params['simulation_step']:
			traci.simulationStep()
			# Your Simulation Script here
			print("Step:" + str(step))
			step += 1
			time.sleep(1)
			progress_recorder.set_progress(step, params['simulation_step'])
		traci.close()
		print("¡La simulacion ha terminado con exito!")
	except ImportError:
		pass

	return '¡La simulacion ha terminado con exito!'
