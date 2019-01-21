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
		os.environ["SUMO_HOME"] = "/home/fernando/sumo-git"
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
		OUT = MEDIA + params['simulation_path'] + "output/resclima_sumo_trace.xml"
		COUT = MEDIA + params['simulation_path'] + "output/resclima_emission_output.xml"
		sumoBinary = "/home/fernando/sumo-git/bin/sumo"
		sumoCmd = [sumoBinary, "-c", PATH, "--fcd-output", OUT, "--emission-output", COUT]
		traci.start(sumoCmd, port=8888)
		print("Realizando la Simulacion...")
		step = 0
		while step < params['simulation_step']:
			traci.simulationStep()
			# Your Simulation Script here
			print("Step:", step)
			step += 1
			time.sleep(1)
			progress_recorder.set_progress(step, params['simulation_step'])
		traci.close()
		sys.exit("SUMO_HOME enviroment variable declared")
	except ImportError:
		sys.exit("please declare environment variable 'SUMO_HOME'")

	return 'done'
