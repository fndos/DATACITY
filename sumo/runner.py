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

from __future__ import absolute_import
from __future__ import print_function


import os, sys
import subprocess
import shutil

os.environ["SUMO_HOME"] = "/home/fernando/sumo-git"

try:
	tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
	sys.path.append(tools)
	import sumolib
	from sumolib.miscutils import getFreeSocketPort
	import traci
	PORT = sumolib.miscutils.getFreeSocketPort()
	sumoBinary = "/home/fernando/sumo-git/bin/sumo"
	sumoCmd = [sumoBinary, "-c", "osm.sumocfg", "--fcd-output", "resclima_sumo_trace.xml"]
	traci.start(sumoCmd, port=PORT)
	print("Realizando Simulacion")
	step = 0
	while step < 5:
	   traci.simulationStep()
	   # Your Script here
	   print("Step:", step)
	   step += 1
	traci.close()
	sys.exit("SUMO_HOME enviroment variable declared")
except ImportError:
	sys.exit("please declare environment variable 'SUMO_HOME'")
