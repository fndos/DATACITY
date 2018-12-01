var vector_layer = undefined;
var map_container, 
legend_container, 
styles_container, 
attributes_container, 
vectorlayer_id;


function createLegendRow(value,symbolizer){
	var row = document.createElement("div");
	
	var text = document.createElement("h5");
	text.innerHTML = value;

	var symb = document.createElement("div");
	console.log(symbolizer)



	var polygon = null;
	for (var key in symbolizer) {
		if (symbolizer.hasOwnProperty(key)){
			polygon = symbolizer[key]
			break;
		}
   	}

	symb.style.width = "15px";
	symb.style.height = "15px";
	symb.style.backgroundColor = polygon.fillColor;
	symb.style.borderWidth = polygon.strokeWidth;
	symb.style.borderStyle = "solid";
	symb.style.borderColor = "black";


	row.appendChild(symb);
	row.appendChild(text)
	return row;
}

function renderLegend(container_legend,rules){

	var container = document.getElementById(container_legend);
	container.innerHTML = "";

	var i = 0; length = rules.length;


	for (i;i<length;i++){
		var rule = rules[i];
		var value = rule.name;
		var symbolizer = rule.symbolizer;
		var row = createLegendRow(value,symbolizer);
		container.appendChild(row);
	}

}



function applyStyle(sld){
	var format = new OpenLayers.Format.SLD();
	var sld = format.read(sld);
	var namedLayers = sld.namedLayers;
	var namedLayer = null;
	for (var key in namedLayers) {
		if (namedLayers.hasOwnProperty(key)){
			namedLayer = namedLayers[key]
			break;
		}
   	}

	var styles = namedLayer.userStyles;
	var style = styles[0];
	vector_layer.styleMap.styles["default"] = style;
	vector_layer.redraw();

	renderLegend("legend",style.rules);
}


function requestStyle(style_id){
	var url = "/vector/export_style/" + style_id;
	var request = $.get(url);
	request.done(function(sld){
		applyStyle(sld)
	})
}


function cleanStyleList(styles_container){
	var selector = "#"+styles_container+ " > ul > li";
	var styles = document.querySelectorAll(selector);

	for (var i=0; i < styles.length; i++){
		style = styles[i]
		console.log("limpio", style.dataset.id)
		style.className = "list-group-item";
	}
}

function enabledStyle(styles_container){

	var selector = "#"+styles_container+ " > ul > li";
	var styles = document.querySelectorAll(selector);

	for (var i=0; i < styles.length; i++){
		style = styles[i]
		style_id = style.dataset.id;

		
		if(i==0){
			style.className = "list-group-item active";
			requestStyle(style_id);
		}
		else{
			style.className = "list-group-item";
		}


		style.addEventListener("click",function(event){
			var target = event.target;
			style_id = target.dataset.id;
			requestStyle(style_id);
			cleanStyleList(styles_container)
			target.className = "list-group-item active";
		});

	}

}


function initMap(map_container){
	var map = new OpenLayers.Map({
		div:map_container,
		projection:"EPSG:3857",
		displayProjection: new OpenLayers.Projection("EPSG:4326"),
		numZoomLevels:11,
		units: 'm'
	});
	var osm = new OpenLayers.Layer.OSM("OSM");
	map.addLayer(osm);
	map.zoomToMaxExtent();
	return map;
}


var layerListeners = {
    featureclick: function(e) {
    	var attributes = e.feature.attributes;
        var container = document.getElementById(attributes_container);
        container.innerHTML = "";

        var table = document.createElement("table");
        table.className = "table table-striped";
        
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


        var tbody = document.createElement("tbody");

        for (var attr in attributes) {
   			if (attributes.hasOwnProperty(attr)){
      			var value = attributes[attr];

      			var tr = document.createElement("tr");
      			var td_1 = document.createElement("td");
      			var td_2 = document.createElement("td");

      			td_1.innerHTML = "" + attr;
      			td_2.innerHTML = "" + value;

				tr.appendChild(td_1);
        		tr.appendChild(td_2);
        		tbody.appendChild(tr);
   			}
		}
		table.appendChild(tbody);
		container.appendChild(table);

        return false;
    },
    nofeatureclick: function(e) {
        var container = document.getElementById(attributes_container);
        container.innerHTML = "<h2>Click en un feature</h2>";
    }
};


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
	console.log(minX,minY,maxX,maxY)
	return [minX,minY,maxX,maxY]
}


function renderFeatureLayer(data,map){
	console.log(data.bbox)
	var extent = getExtent(data.bbox);   	
   	map.zoomToExtent(extent);

	var geojson_format = new OpenLayers.Format.GeoJSON();

	vector_layer = new OpenLayers.Layer.Vector("layer",{
			projection: new OpenLayers.Projection("EPSG:900913"),
			eventListeners: layerListeners
		});

	var features = geojson_format.read(data);
	
	for (i=0; i<features.length; i++){
		feature = features[i];
		feature.geometry.transform('EPSG:4326','EPSG:900913');
   	}

   	vector_layer.addFeatures(features);

   	map.addLayer(vector_layer);
   	enabledStyle("styles");
}


function requestLayer(vectorlayer_id,map){
	var url = "/vector/geojson/" + vectorlayer_id
	var request = $.get(url);
	request.done(function(data){
		renderFeatureLayer(data,map);
	});
}


function init(options){

	map_container = options["map_container"]
	legend_container = options["legend_container"]
	styles_container = options["styles_container"]	
	attributes_container = options["attributes_container"]
	vectorlayer_id = options["vectorlayer_id"]

	var map = initMap(map_container);
	requestLayer(vectorlayer_id,map);

}
