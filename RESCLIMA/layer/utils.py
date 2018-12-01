from osgeo import ogr


# retorna el bbox de una capa
# como poligono GEOSGeometry
def getLayerBBox(minX,minY,maxX,maxY):
    #se crea un anillo
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint_2D(minX,minY);
    ring.AddPoint_2D(minX,maxY);
    ring.AddPoint_2D(maxX,maxY)
    ring.AddPoint_2D(maxX,minY)
    ring.AddPoint_2D(minX,minY);
    # se crea el poligono
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)
    
    poly = GEOSGeometry(poly.ExportToWkt())
    return poly