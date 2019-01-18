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

    # SIMULACION START
    #!/usr/bin/env python
    # Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
    # Copyright (C) 2008-2018 German Aerospace Center (DLR) and others.
    # This program and the accompanying materials
    # are made available under the terms of the Eclipse Public License v2.0
    # which accompanies this distribution, and is available at
    # http://www.eclipse.org/legal/epl-v20.html
    # SPDX-License-Identifier: EPL-2.0

    # @file    runner.py
    # @author  Daniel Krajzewicz
    # @author  Michael Behrisch
    # @date    2007-10-25
    # @version $Id$

    os.environ["SUMO_HOME"] = "/home/fernando/sumo-git"

    try:
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
      PATH = MEDIA + "/simulation/user_17/osm.sumocfg"
      OUT = MEDIA + "/simulation/user_17/output/resclima_sumo_trace.xml"
      sumoBinary = "/home/fernando/sumo-git/bin/sumo"
      sumoCmd = [sumoBinary, "-c", PATH, "--fcd-output", OUT]
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
    except:
      sys.exit("please declare environment variable 'SUMO_HOME'")

    # SIMULACION END
    return 'done'
