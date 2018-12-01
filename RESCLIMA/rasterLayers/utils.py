# -*- encoding: utf-8 -*-
from osgeo import osr
from django.contrib.gis.geos import Polygon

def getBBox(datasource):
	gt = datasource.GetGeoTransform()
	if gt==None:
		return None
	cols = datasource.RasterXSize
	rows = datasource.RasterYSize
	ext=[]
	xarr=[0,cols]
	yarr=[0,rows]

	for px in xarr:
		for py in yarr:
			x=gt[0]+(px*gt[1])+(py*gt[2])
			y=gt[3]+(px*gt[4])+(py*gt[5])
			ext.append([x,y])
		yarr.reverse()

	# se reproyecta a EPSG:4326
	src_srs=osr.SpatialReference()
	src_srs.ImportFromWkt(datasource.GetProjection())
	tgt_srs = osr.SpatialReference()
	tgt_srs.ImportFromEPSG(4326)

	trans_coords=[]
	transform = osr.CoordinateTransformation(src_srs,tgt_srs)
	for x,y in ext:
		x,y,z = transform.TransformPoint(x,y)
		trans_coords.append([x,y])

	minX = trans_coords[0][0]
	minY = trans_coords[1][1]
	maxX = trans_coords[2][0]
	maxY = trans_coords[0][1]

	coords = ((minX,minY),(minX,maxY),
		(maxX,maxY),(maxX,minY),(minX,minY))
	bbox = Polygon(coords)
	return bbox
