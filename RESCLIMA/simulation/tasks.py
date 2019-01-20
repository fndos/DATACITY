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
def simulation_task(self):
	progress_recorder = ProgressRecorder(self)

	try:
		os.environ["SUMO_HOME"] = "/home/fernando/sumo-git"
		tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
		sys.path.append(tools)
		import sumolib
		import traci
		MEDIA = settings.MEDIA_ROOT
		try:
		  os.mkdir(os.path.join(MEDIA + '/simulation/user_17/', 'output'))
		except OSError as e:
		  if e.errno != errno.EEXIST:
			  raise
		PATH = MEDIA + "/simulation/user_17/simulatino_4/osm.sumocfg"
		OUT = MEDIA + "/simulation/user_17/simulatino_4/output/resclima_sumo_trace.xml"
		COUT = MEDIA + "/simulation/user_17/simulation_4/output/resclima_emission_output.xml"
		sumoBinary = "/home/fernando/sumo-git/bin/sumo"
		sumoCmd = [sumoBinary, "-c", PATH, "--fcd-output", OUT, "--emission-output", COUT]
		traci.start(sumoCmd, port=8888)
		print("Realizando Simulacion")
		step = 0
		while step < 5:
			traci.simulationStep()
			# Your Script here
			print("Step:", step)
			step += 1
			time.sleep(1)
			progress_recorder.set_progress(step, 5)
		traci.close()
		sys.exit("SUMO_HOME enviroment variable declared")
	except ImportError:
		sys.exit("please declare environment variable 'SUMO_HOME'")

	return 'done'
