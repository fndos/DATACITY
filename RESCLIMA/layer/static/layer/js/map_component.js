/*
Funcion que recibe un objeto OpenLayers.Layer.Vector
y una  posicion  (lon,lat).  Buscara  dentro de  los 
features de la capa y retornara el feature  que con-
tenga la posicion. Si no encuentra un feature retor-
na null.
*/
function searchFeature(vectorlayer,lon,lat){
	var features = vectorlayer.features;
	for(var i=0;i<features.length;i++){
		var feature = features[i];
		var bounds = feature.geometry.bounds;
		var left = bounds["left"];
		var right = bounds["right"];
		var bottom = bounds["bottom"];
		var top = bounds["top"];
		var ofset = store.map.getResolution()*5;
		if(left==right){
			left -= ofset;
			right += ofset;
		}
		if(bottom==top){
			bottom -= ofset;
			top += ofset;
		}
		if(lon >= left & lon<= right
			& lat >= bottom & lat <= top){
			return feature;
		}
	}
	return null
}

/*
Funcion que crea una tabla HTML que muestra los
atributos de un feature. Retorna la tabla  como
un string HTNL
*/
function createAttributeTable(attributes){
	// contenedor
	var content = document.createElement("div");
	var table = document.createElement("table");
	table.className = "bordered";
	// cabezera de la tabla: | Atributo | Valor |
	var thead = document.createElement("thead");
	var tr = document.createElement("tr");
	var th_1 = document.createElement("th");
	th_1.innerHTML = "Atributo";
	var th_2 = document.createElement("th");
	th_2.innerHTML = "Valor";

	tr.appendChild(th_1);
	tr.appendChild(th_2);
	thead.appendChild(tr);
	table.appendChild(thead);

	// cuerpo de la tabla
	var tbody = document.createElement("tbody");
	// por cada atributo se crea una fila de la
	// tabla
	for (var attr in attributes) {
		if (attributes.hasOwnProperty(attr)){
			var value = attributes[attr];

			var tr = document.createElement("tr");
			var td_1 = document.createElement("td");
			var td_2 = document.createElement("td");

			td_1.innerHTML = String(attr);
			td_2.innerHTML = String(value);

			tr.appendChild(td_1);
			tr.appendChild(td_2);
			tbody.appendChild(tr);
		}
	}
	table.appendChild(tbody);
	content.appendChild(table);
	// se retorna la tabla como un string
	return content.innerHTML;
}

/* 
Metodo que obtiene el extent de una capa.
Recibe un json con el bbox de la capa. El extent
es un array con los limites de la capa
[minX,minY,maxX,maxY]
*/
function getExtent(bbox_json){
	var geojson_format = new OpenLayers.Format.GeoJSON();
	var polygon = geojson_format.read(bbox_json)[0];
	polygon.geometry.transform('EPSG:4326','EPSG:900913');
	var coords = polygon.geometry.components[0]
	coords = coords.components
	var minX,minY,maxX,maxY
	minX = coords[0]["x"]
	minY = coords[0]["y"]
	maxX = coords[2]["x"]
	maxY = coords[2]["y"]
	return [minX,minY,maxX,maxY]
}

/*Objeto  con  funciones  para 
manipulacion de capas vectoriales
Recibe: el mapa de OpenLayers 
y la capa
*/
var VectorLayer = function(map,layer){

	// Metodo para obtener los datos de una capa
	this.loadLayer=function(){
		// se recupera la capa
		// compartida
		var id_layer = layer["id"];
		// se realiza la peticion al servidor
		var url = "/vector/geojson/" + id_layer;
		var request = $.get(url);
		// TODO - implementar callbacks de error
		request.done(function(response){
			renderFeatureLayer(response);
		});
	}

	// Metodo que renderiza la capa
	function renderFeatureLayer(data){ 	
		var id_layer = layer["id"]

		//se obtiene el extent de la capa
		var extent = getExtent(layer["bbox"]);
		// se guarda el extent
		layer["extent"] = extent;

		// parser de geo_json
		var geojson_format = new OpenLayers.Format.GeoJSON();


		// se crea una capa vectorial de OpenLayers
		// con proyeccion EPSG:900913
		var vectorlayer = new OpenLayers.Layer.Vector(id_layer,{
			projection: new OpenLayers.Projection("EPSG:900913"),
			rendererOptions: {zIndexing: true}
		});
		// con el parser de geojson se obtienen los features
		// de la capa
		var features = geojson_format.read(data);
		// los features estan en EPSG:4326 
		// y deben ser transformados a EPSG:900913
		for (i=0; i<features.length; i++){
			feature = features[i];
			feature.geometry.transform('EPSG:4326','EPSG:900913');
		}
		// se agregan los features a la capa
		vectorlayer.addFeatures(features);

		
		
		// se agrega la capa al mapa
		map.addLayer(vectorlayer);
		// si el indice de la capa es 0
		// se realiza un zoom a su bbox
		var index = layer["index"];
		if(index==0){
			map.zoomToExtent(extent);
		}

		// se configura el zIndex de la capa
		var zIndex = layer["zIndex"];
		vectorlayer.setZIndex(zIndex);
		// se actualiza el estado de la capa
		layer["state"]="loaded";
		// se guarda una referencia a la capa
		// de OpenLayers
		layer["openlayer_layer"]=vectorlayer;
		// se obtiene el estilo seleccionado
		// de la capa
		var selectedStyle = layer["currentStyle"];
		if(selectedStyle){
			requestStyle(selectedStyle);
		}

	}

	// Metodo para obtener el archivo SLD
	// que define el estilo
	function requestStyle(style){
		var style_id = style["id"]
		var url = "/vector/export_style/" + style_id;
		var request = $.get(url);
		request.done(function(sld){
			applyStyle(style,sld)
		})
	}

	// Metodo Publico de requestStyle
	this.requestStyle = function(style){
		requestStyle(style);
	}

	// Metodo que aplica el estilo a la capa
	function applyStyle(layer_style,sld){
		// parser de sld
		var format = new OpenLayers.Format.SLD();
		// se obtiene un objeto con las reglas del estilo
		var sld = format.read(sld);
		console.log("sld de capa", layer_style,sld)
		// se obtiene la propiedad  namedLayer del
		// objeto sld
		var namedLayers = sld.namedLayers;
		var namedLayer = null;
		for (var key in namedLayers) {
			if (namedLayers.hasOwnProperty(key)){
				namedLayer = namedLayers[key]
				break;
			}
		}
		// se obtiene el estilo
		var styles = namedLayer.userStyles;
		var style = styles[0];
		var vectorlayer = layer["openlayer_layer"];
		// se aplica el estilo a la capa de OpenLayers
		vectorlayer.styleMap.styles["default"] = style;
		// se crea la leyenda
		createLegend(layer_style,style.rules);
		// se redibuja la capa
		vectorlayer.redraw();
	}

	// Este metodo recibe el objeto rules
	// lo transforma a un objeto mas simple
	// y lo guarda en el estilo seleccionado
	// del shared_layer
	function createLegend(layer_style,rules){
		var i = 0; 
		var length = rules.length;
		// se obtiene la leyenda
		var legend = layer_style["legend"];
		legend.splice(0,legend.length);
		// se recorren las reglas
		for (i;i<length;i++){
			var rule = rules[i];
			var value = rule.name;
			var symbolizer = rule.symbolizer;
			var color = getColor(symbolizer);
			// se guarda el color y el label
			legend.push({
				"color":color,
				"label":value,
			});
		}
	}

	// Este metodo recibe un objeto symbolizer
	// y retorna el color
	function getColor(symbolizer){
		var polygon = null;
		for (var key in symbolizer) {
			if (symbolizer.hasOwnProperty(key)){
				polygon = symbolizer[key]
				break;
			}
		}
		if (polygon.hasOwnProperty("fillColor")){
			return polygon.fillColor
		}
		if(polygon.hasOwnProperty("strokeColor")){
			return polygon.strokeColor
		}
		return polygon.fillColor;
	}

}

/*Objeto con funciones para 
manipulacion de capas raster
Recibe: el mapa de OpenLayers
y la capa
*/
var RasterLayer = function(map,layer){
	
	// Metodo para obtener los datos de una capa
	this.loadLayer = function(){
		// capa compartida
		var id_layer = layer["id"]
		//se obtiene el extent de la capa
		var extent = getExtent(layer["bbox"]);
		// se guarda el extent
		layer["extent"] = extent;
		// se crea una capa raster de OpenLayers
		var rasterlayer = new OpenLayers.Layer.TMS(id_layer,
					"/tms/",
					{serviceVersion: "1.0",
					layername: id_layer,
					type: 'png',
					isBaseLayer: false,
					rendererOptions: {zIndexing: true}
				});
		map.addLayer(rasterlayer);

		// si el index es cero
		// se hace zoom a la capa
		var index = layer["index"];
		if(index==0){
			map.zoomToExtent(extent);
		}
		// se configura el zIndex
		var zIndex = layer["zIndex"];
		rasterlayer.setZIndex(zIndex);
		// se actualiza el estado de la capa
		layer["state"]="loaded";

		// se guarda una referencia a la capa
		// de OpenLayers
		layer["openlayer_layer"]=rasterlayer;
		// se obtiene el estilo seleccionado
		// de la capa
		var selectedStyle = layer["currentStyle"];
		if(selectedStyle){
			requestStyle(selectedStyle);
		}
	}

	// Metodo que carga informacion del estilo 
	// de la capa
	function requestStyle(style){
		var style_id = style["id"]
		var url = "/raster/style_legend/" + style_id;
		var request = $.get(url);
		request.done(function(legend){
			createLegend(style,legend);
		})
	}

	function createLegend(layer_style,legend_json){
		var legend = layer_style["legend"];
		legend.splice(0,legend.length);

		for (i=0;i<legend_json.length;i++){
			var row = legend_json[i];
			// se guarda el color y el label
			legend.push(row);
		}

	}

	// Metodo Publico de requestStyle
	this.requestStyle = function(style){
		requestStyle(style);
	}

}


Vue.component("map_component",{
	template: `
		<div id="map_component" style="height:700px;">
			<!-- Contenedor del mapa de OpenLayers -->
			<div id="map_container" style="width:100%;height:100%;">
				<!-- Controlador del zoom del mapa personalizado-->
				<div id="customZoom">
					<a href="#customZoomIn" id="customZoomIn">+</a>
					<a href="#customZoomOut" id="customZoomOut">-</a>
				</div>
			</div>
		</div>
	`,
	mounted(){
		//referencia al componente
		var self = this;
		/*Objeto con listeners del click del mapa*/
		var layerListeners = {
			click: function(e){
				self.clickHandler(e);
			}
		}

		// se inicializa el mapa
		var map = new OpenLayers.Map({
			div:"map_container",
			projection:"EPSG:3857",
			displayProjection: new OpenLayers.Projection("EPSG:4326"),
			numZoomLevels:11,
			units: 'm',
			controls:[],
			eventListeners:layerListeners
		});

		//Controles del mapa
		var controls = [
			new OpenLayers.Control.Navigation({
				dragPanOptions: {
					enableKinetic: true
				}
			}),
			new OpenLayers.Control.Attribution(),
			new OpenLayers.Control.Zoom({
				zoomInId: "customZoomIn",
				zoomOutId: "customZoomOut"
			})
		]
		map.addControls(controls);

		// se agrega una capa de OpenStreetMap
		var osm = new OpenLayers.Layer.OSM("OSM");
		map.addLayer(osm);
		// se la configura para que esta sea la capa base
		osm.setZIndex(0);
		map.zoomToMaxExtent();
		
		// se guarda la referencia del mapa
		this.shared.map = map;
		// se reacciona al evento 
		// que se dispara cuando
		// se obtienen los metadatos de una capa
		this.$root.$on('layer_metadata', this.loadLayer);
		// se reacciona al evento
		// que se dispara cuando se cambia el estilo
		this.$root.$on("update_style",this.updateStyle);
	},
	data(){
		return {
			shared:store
		}
	},
	methods:{
		/*Metodo que se ejecuta cuando
		se actualizan los metadatos de la capa.
		Dependiendo del tipo de capa (vector,raster)
		se piden los datos y se las muestra en el mapa*/
		loadLayer(layer){
			// se guarda referencia al componente
			var self = this;
			var map = this.shared.map;
			/*Se calcula el zIndex de la capa.
			En OpenLayers el zIndex define la posicion
			de la capa. zIndex=0 es la capa base y asi 
			sucesivamente. Se quiere que la capa con index=0
			sea la capa mas superior, y asi en adelante, asi
			que se calcula el zIndex de la capa
			*/
			var numLayers = this.shared.layers.length;
			var index = layer["index"];
			var zIndex = numLayers - index;
			layer["zIndex"]=zIndex;
			if (layer["type"]=="vector"){
				// se crea un objeto con metodos para el manejo
				// de capas vectoriales
				var vectorlayer = new VectorLayer(map,layer);
				vectorlayer.loadLayer();
			}
			if(layer["type"]=="raster"){
				// se crea un objeto con metodos para el manejo
				// de capas raster
				var rasterlayer = new RasterLayer(map,layer);
				rasterlayer.loadLayer();
			}
		},
		/*Metodo que se ejecuta cuando el usuario selecciona
		un estilo de la capa. Se aplicara ese estilo a la capa
		actual*/
		updateStyle(){
			// se recupera la capa actual
			var currentLayer = this.shared.currentLayer;
			// se recupera el estilo de la capa actual
			var currentStyle = currentLayer.currentStyle;
			var map = this.shared.map;
			if(currentLayer["type"]=="vector"){
				var vectorlayer = new VectorLayer(map,currentLayer);
				vectorlayer.requestStyle(currentStyle);
			}
			if(currentLayer["type"]=="raster"){
				var rasterlayer = new RasterLayer(map,currentLayer);
				rasterlayer.requestStyle(currentStyle);
			}
		},
		/*Metodo que se ejecuta cuando el usuario da click
		en el mapa. Se obtendra el feature seleccionado y
		se mostrara una tabla con sus atributos*/
		clickHandler(e){
			var map = this.shared.map;
			// se obtiene la coordenada del click
			var lonlat = map.getLonLatFromPixel(e.xy);
			var lon = lonlat.lon;
			var lat = lonlat.lat;
			var layers = store.layers;
			/* se busca si en las capas vectoriales, 
			el punto esta dentro de su extent*/
			var features = []
			for(var i=0;i<layers.length;i++){
				var layer = layers[i];
				// solo se usan las capas vectoriales
				if(layer["type"]!="vector"){
					continue;
				}
				var extent = layer["extent"]
				// si a la capa aun no se le ha calculado
				// el extent, no se hace nada
				if(!extent){
					continue;
				}
				if(extent.length<4){
					continue;
				}
				// si el punto esta dentro de la capa
				if(lon >= extent[0] & lon <= extent[2]
				   & lat >= extent[1] & lat <= extent[3]){
					// se recupera la capa de OpenLayers
					var vectorlayer = layer["openlayer_layer"];
					// se busca un feature que contenga el punto
					var feature = searchFeature(vectorlayer,lon,lat);
					if(feature){
						// se guarda el feature, junto con el zIndex de la capa
						features.push({"feature":feature,"zIndex":layer["zIndex"]});
					}
				}
			}
			// si no se encontraron features no se hace nada
			if(features.length==0){
				return;
			}
			// se ordenan los features de acuerdo a su zIndex
			// de forma descendiente
			features.sort(function(a,b){
				za = a["zIndex"];
				zb = b["zIndex"];
				return za - zb;
			});
			// se obtiene el feature con zIndex mas alto
			// se le dara prioridad a ese feature
			var selected = features[0];
			// muestra una tabla con los atributos del feature
			this.showAttributes(selected["feature"],lon,lat);

		},
		/*Crea un popup con la tabla de atributos de un feature.
		Y lo coloca en (lon,lat)
		*/
		showAttributes(feature,lon,lat){
			var id = feature.id;
			var attributes = feature.attributes;
			// se crea la tabla HTML
			var content = createAttributeTable(attributes);
			// se crea el popup
			popup = new OpenLayers.Popup(id,
				new OpenLayers.LonLat(lon,lat),
				new OpenLayers.Size(300,200),
				content,true);
			// se muestra el popup
			this.shared.map.addPopup(popup);
		}
	},
})



