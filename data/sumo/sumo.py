import os, sys

os.environ["SUMO_HOME"] = "/home/fernando/sumo-git"

if 'SUMO_HOME' in os.environ:
	tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
	sys.path.append(tools)
	import sumolib
	sys.exit("SUMO_HOME enviroment variable declared")

	# import the library
	import sumolib
	# parse the net
	net = sumolib.net.readNet('sample.net.xml')

	# retrieve the coordinate of a node based on its ID
	print net.getNode('myNodeID').getCoord()

	# retrieve the successor node ID of an edge
	nextNodeID = net.getEdge('myEdgeID').getToNode().getID()

	# compute the average length
	speedSum = 0.0
	edgeCount = 0
	for edge in sumolib.output.parse('sample.edg.xml', ['edge']):
		speedSum += float(edge.speed)
		edgeCount += 1
	avgSpeed = speedSum / edgeCount

	# compute the median length using the Statistics module
	edgeStats = sumolib.miscutils.Statistics("edge speeds")
	for edge in sumolib.output.parse('sample.edg.xml', ['edge']):
		edgeStats.add(float(edge.speed))
	avgSpeed = edgeStats.median()

	# (requires module pyproj to be installed)
	# for larger networks rtree is also strongly recommended
	radius = 0.1
	x, y = net.convertLonLatXY(lon, lat)
	edges = net.getNeighboringEdges(x, y, radius)
	# pick the closest edge
	if len(edges) > 0:
		distancesAndEdges = sorted([(dist, edge) for edge, dist in edges])
		dist, closestEdge = distancesAndEdges[0]

	for route in sumolib.output.parse_fast("sample.rou.xml", 'route', ['edges']):
		edge_ids = route.edges.split()
		# do something with the vector of edge ids

	net = sumolib.net.readNet('sample.net.xml')

	# network coordinates (lower left network corner is at x=0, y=0)
	x, y = net.convertLonLat2XY(lon, lat)
	lon, lat = net.convertXY2LonLat(x, y)

	# raw UTM coordinates
	x, y = net.convertLonLat2XY(lon, lat, True)
	lon, lat = net.convertXY2LonLat(x, y, True)

else:
	sys.exit("Please declare environment variable 'SUMO_HOME'")
