from lxml import etree
from os.path import join
from models import Style
import traceback

# Transforma un archivo sld version 1.1.0 a 
# un archivo sld version 1.0.0
# recibe el contenido del archivo en un string
# retorna un string con el contendio del sld resultante

def transformSLD(sld):

    # Se crea un string con la cabecera
    new_sld = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
    new_sld = "<sld:StyledLayerDescriptor version=\"1.0.0\" "
    new_sld = new_sld + "xmlns:sld=\"http://www.opengis.net/sld\" "
    new_sld = new_sld + "xmlns:ogc=\"http://www.opengis.net/ogc\" "
    new_sld = new_sld + "xmlns:gml=\"http://www.opengis.net/gml\" "
    new_sld = new_sld + "xmlns:xlink=\"http://www.w3.org/1999/xlink\" "
    new_sld = new_sld + "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" "
    new_sld = new_sld + "xsi:schemaLocation=\"http://www.opengis.net/sld http://schemas.opengis.net/sld/1.0.0/StyledLayerDescriptor.xsd\">"

    # con la libreria lxml se parsea el string sld
    root = etree.fromstring(sld);
    # se obtienen los hijos del root
    children = root.getchildren();

    # en el string children_str se agregan los hijos
    children_str = ""
    for child in children:
        children_str = children_str + etree.tostring(child);
    
    # se agrega el string de los hijos a la cabecera
    new_sld = new_sld + children_str
    # se cierra el ultimo tag
    new_sld = new_sld + "</sld:StyledLayerDescriptor>"

    # se reemplazan los prefix "se" por "sld"
    new_sld = new_sld.replace("se:","sld:");
    # se reemplazan los prefix "SvgParameter" por "CssParameter" 
    new_sld = new_sld.replace("SvgParameter","CssParameter");

    
    return new_sld

# Parsea un archivo sld solo de raster
# devuelve un diccionario con la informacion
# del color, el label, opacity y quantity
def parseRasterSLD(sld):
    root = etree.fromstring(sld);
    xpath = "sld:UserLayer/sld:UserStyle/sld:FeatureTypeStyle/"
    xpath = xpath + "sld:Rule/sld:RasterSymbolizer/sld:ColorMap"
    colorMaps = root.findall(xpath,namespaces={"sld":"http://www.opengis.net/sld"})
    
    if (len(colorMaps)==0):
        return None
    
    colorMap = colorMaps[0]

    try:
        result = []
        for x in colorMap:
            entry = {}
            entry["color"] = x.get("color")
            entry["label"] = x.get("label")
            entry["opacity"] = x.get("opacity")
            entry["quantity"] = float(x.get("quantity"))
            result.append(entry)
    except:
        traceback.print_exc()
        return None

    return result


# retorna un diccionario con la informacion
# del color, el label, opacity y quantity del
# archivo sld de un style de tipo raster
def getColorMap(style):
    file_path = style.file_path;
    file_name = style.file_name;
    fullName = join(file_path,file_name);
    f = open(fullName,'r');
    sld = f.read()
    colorMap = parseRasterSLD(sld)
    return colorMap  