from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from os.path import join
from rasterLayers.models import RasterLayer
from style.models import Style
from style.utils import getColorMap
import traceback
import math
import mapnik


MAX_ZOOM_LEVEL = 20
TILE_WIDTH     = 256
TILE_HEIGHT    = 256

def root(request):
	try:
		baseURL = request.build_absolute_uri()
		xml = []
		xml.append('<?xml version="1.0" encoding="utf-8" ?>')
		xml.append('<Services>')
		xml.append('<TileMapService title="RESCLIMA TMS" ' +
		       'version="1.0" href="' + baseURL + '1.0"/>')
		xml.append('</Services>')
		return HttpResponse("\n".join(xml), content_type="text/xml")
	except:
		traceback.print_exc()
		return HttpResponse("Error")

def service(request, version):
	try:
		if version != "1.0":
			raise Http404
		baseURL = request.build_absolute_uri()
		xml = []
		xml.append('<?xml version="1.0" encoding="utf-8" ?>')
		xml.append('<TileMapService version="1.0" services="' + baseURL + '">')
		xml.append('<Title>RESCLIMA TMS</Title>')
		xml.append('<Abstract></Abstract>')
		xml.append('<TileMaps>')
		
		id = str(1)
		xml.append('<TileMap title="' + "Prect" + '"')
		xml.append('srs="EPSG:4326"')
		xml.append('href="'+baseURL+'/'+id+'"/>')
		
		xml.append('</TileMaps>')
		xml.append('</TileMapService>')
		return HttpResponse("\n".join(xml), content_type="text/xml")
	except:
		traceback.print_exc()
	return HttpResponse("Error")


def tileMap(request, version, rasterlayer_id):

	if version != "1.0":
		raise Http404

	try:
		baseURL = request.build_absolute_uri()
		xml = []
		xml.append('<?xml version="1.0" encoding="utf-8" ?>')
		xml.append('<TileMap version="1.0" ' +
		           'tilemapservice="' + baseURL + '">')
		xml.append('<Title>' + "prect" + '</Title>')
		xml.append('<Abstract></Abstract>')
		xml.append('<SRS>EPSG:4326</SRS>')
		xml.append('<BoundingBox minx="-180" miny="-90" maxx="180" maxy="90"/>')
		xml.append('<Origin x="-180" y="-90"/>')
		xml.append('<TileFormat width="' + str(TILE_WIDTH) +
		           '" height="' + str(TILE_HEIGHT) + '" ' +
		           'mime-type="image/png" extension="png"/>')
		xml.append('<TileSets profile="global-geodetic">')
		
		for zoomLevel in range(0, MAX_ZOOM_LEVEL+1):
			unitsPerPixel = _unitsPerPixel(zoomLevel)
			xml.append('<TileSet href="' + 
			           baseURL + '/' + str(zoomLevel) +
			           '" units-per-pixel="'+str(unitsPerPixel) +
			           '" order="' + str(zoomLevel) + '"/>')
		xml.append('</TileSets>')
		xml.append('</TileMap>')
		return HttpResponse("\n".join(xml), content_type="text/xml")
	except:
		traceback.print_exc()
		return HttpResponse("Error")


def _unitsPerPixel(zoomLevel):
    # ancho del mundo = 20026376.39 + 20048966.10 = 40075342.49
    # 40075342.49/256=156544.3066
    return 156544.3066/math.pow(2,zoomLevel)


def tile(request, version, rasterlayer_id, zoom, x, y):
	try:
		rasterlayer = RasterLayer.objects.get(id=rasterlayer_id)

		if version != "1.0":
			raise Http404
		
		zoom = int(zoom)
		x    = int(x)
		y    = int(y)


		if zoom < 0 or zoom > MAX_ZOOM_LEVEL:
			raise Http404

		xExtent = _unitsPerPixel(zoom) * TILE_WIDTH
		yExtent = _unitsPerPixel(zoom) * TILE_HEIGHT


		minLong = x * xExtent -20026376.39
		minLat = y * yExtent - 20026376.39  
		maxLong = minLong + xExtent
		maxLat = minLat + yExtent

		map = mapnik.Map(TILE_WIDTH, TILE_HEIGHT, "+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +units=m +k=1.0 +nadgrids=@null +no_defs")
		map.background = mapnik.Color("#00000000")
		raster = mapnik.Layer("raster");
		raster.srs = "+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0.0 +k=1.0 +units=m +nadgrids=@null +no_defs +over"

		# se carga el archivo
		file_path = rasterlayer.file_path
		file_name = rasterlayer.file_name
		file_format = rasterlayer.file_format
		ext = file_format
		file_name = file_name.replace(ext,"-proj"+ext)
		fullName = join(file_path,file_name)
		numBands = rasterlayer.numBands

		# se obtiene el estilo
		layer_styles = Style.objects.filter(layers__id=rasterlayer.id)
		if numBands == 1 and layer_styles.count()==1:
			raster.datasource = mapnik.Gdal(file=fullName,band=1)
		else:
			raster.datasource = mapnik.Gdal(file=fullName)

		style = mapnik.Style()
		rule = mapnik.Rule()

		symbol = mapnik.RasterSymbolizer()

		# agregar estilo si existe
		if layer_styles.count()==1:
			layer_style = layer_styles[0]
			colorMap = getColorMap(layer_style)	
			c = mapnik.RasterColorizer(mapnik.COLORIZER_LINEAR,mapnik.Color(0,0,0,0))

			for entry in colorMap:
				color = entry["color"]
				quantity = entry["quantity"]
				c.add_stop(quantity,mapnik.Color(color))

			symbol.colorizer = c


		rule.symbols.append(symbol)
		style.rules.append(rule)
		map.append_style("estilo",style)
		raster.styles.append("estilo")
		map.layers.append(raster)


		map.zoom_to_box(mapnik.Box2d(minLong, minLat, maxLong, maxLat))
		image = mapnik.Image(TILE_WIDTH, TILE_HEIGHT)
		mapnik.render(map, image)

		imageData = image.tostring('png')
		return HttpResponse(imageData, content_type="image/png")
	except:
		traceback.print_exc()
		return HttpResponse("Error")

