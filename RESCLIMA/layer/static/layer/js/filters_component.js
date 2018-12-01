function getAttributes(layer){
	var vectorlayer = layer["openlayer_layer"];
	var features = vectorlayer.features;
	var feature = features[0];
	var attributes = [];
	attributes.push({"value":"null","name":"-- Atributo --"});

	for(var a in feature.attributes){
		if(feature.attributes.hasOwnProperty(a))
		attributes.push({"value":a,"name":a});
	}
	return attributes;	
}

function renderSelect(id,options){
	var container = document.createElement("div");
	container.className = "col s3";
	var select = document.createElement("select");
	select.style.display = "block";
	select.id = id;

	for(var i=0;i<options.length;i++){
		var option = document.createElement("option");
		option.value = options[i]["value"];
		option.innerText = options[i]["name"];
		select.appendChild(option);
	}
	container.appendChild(select);
	return container;
}


function renderFilter(filter,layer){
	var container = document.createElement("div");
	container.className = "row";

	var attr = document.createElement("div");
	attr.className = "col s3";
	attr.innerText = filter["attribute"];

	var oper = document.createElement("div");
	oper.className = "col s3";
	oper.innerText = filter["operation"];

	var value = document.createElement("div");
	value.className = "col s5";
	value.innerText = filter["value"];

	var btn = renderBtn('remove');
	btn.addEventListener('click',function(e){
		var filters = layer["filters"];
		var index = 0;
		for(var i=0; i<filters.length;i++){
			var f = filters[i];
			if(f==filter){
				index = i;
				break;
			}
		}
		filters.splice(index,1);
		applyFilters(layer);
		var container = document.getElementById("filtersContainer");
		render(layer,container);
	});

	container.appendChild(attr);
	container.appendChild(oper);
	container.appendChild(value);
	container.appendChild(btn);

	return container;
}

function renderInput(id){
	var container = document.createElement("div");
	container.className = "col s5";
	var input = document.createElement("input");
	input.type = "text";
	input.id = id;
	container.appendChild(input);
	return container;
}

function renderBtn(type){
	var container = document.createElement("div");
	container.className = "col s1";
	container.style.cursor = "pointer";
	var i = document.createElement("i");
	i.className = "material-icons";
	i.innerText = type;
	container.appendChild(i);
	return container;
}

function applyFilters(layer){
	var vectorlayer = layer["openlayer_layer"];
	var filters = layer["filters"];
	var features = vectorlayer.features;
	
	for(var i=0; i< features.length;i++){
		var feature = features[i];
		var attributes = feature.attributes;
		feature.style = null;

		for(var j=0; j< filters.length;j++){
			var filter = filters[j];
			var result = evalFilter(attributes,filter);
			// si no pasa el filtro se oculta el feature
			if(result == false){
				feature.style = {'visibility':'none'};
			}
		}
	}
	vectorlayer.redraw();
}

function applyFilter(layer,filter){
	var vectorlayer = layer["openlayer_layer"];
	var features = vectorlayer.features;
	for(var i=0; i< features.length;i++){
		var feature = features[i];
		var attributes = feature.attributes;
		var result = evalFilter(attributes,filter);
		if(result){
			feature.style = {'visibility':'none'};
		}else{
			feature.style = null;
		}
	}
	vectorlayer.redraw();
}

function evalFilter(attributes,filter){
	var attr = filter["attribute"];
	var operation = filter["operation"];
	var value = filter["value"];

	if(operation=="Igual a"){
		return attributes[attr]==value	
	}
	if(operation=="Mayor que"){
		return attributes[attr]>value	
	}
	if(operation=="Menor que"){
		return attributes[attr]<value	
	}
	return false;
}

function render(layer,container){
	container.innerHTML = "";
	var filters = layer["filters"];
	// renderiza los filtros
	var filterList = document.createElement('div');
	filterList.id = "filterList";

	for(var i=0;i<filters.length; i++){
		var filter = filters[i];
		var result = renderFilter(filter,layer);
		filterList.appendChild(result);
	}
	container.appendChild(filterList);

	// etiqueta
	var p = document.createElement("div");
	p.innerText = "Agregar un filtro";
	container.appendChild(p);
	// se obtienen los atributos de la capa
	var attributes = getAttributes(layer);
	// crea un menu para agregar un nuevo
	// filtro
	var newFilterMenu = document.createElement("div");
	newFilterMenu.className = "row";
	// select con los atributos
	var attrs = renderSelect("selectedAttribute",attributes);
	newFilterMenu.appendChild(attrs);
	// se crea un select con las operaciones
	var operations = [
						{"value":"null","name":"-- Operacion --"},
						{"value":"Igual a","name":"Igual a"},
						{"value":"Mayor que","name":"Mayor que"},
						{"value":"Menor que","name":"Menor que"}
					];

	var opers = renderSelect("selectedOperation",operations);
	newFilterMenu.appendChild(opers);
	
	// se crea un input para ingresar el operando del filtro
	var input = renderInput("filterValue");
	newFilterMenu.appendChild(input);
	// boton para agregar un filtro
	var addBtn = renderBtn('add');
	newFilterMenu.appendChild(addBtn);
	container.appendChild(newFilterMenu);


	// se agrega eventos
	addBtn.addEventListener('click',function(event){
		// se agrega un nuevo filtro
		var attrs = document.getElementById("selectedAttribute");
		var attribute = attrs.options[attrs.selectedIndex].value;
		
		if(attribute=="null"){
			return;
		}

		var opers = document.getElementById("selectedOperation");
		var operation = opers.options[opers.selectedIndex].value;

		if(operation=="null"){
			return;
		}
		
		var input = document.getElementById("filterValue");
		var value = input.value;
		if(value==""){
			return;
		}
		if(isNaN(value)==false){
			value = parseFloat(value);
		}

		// se crea y agrega un nuevo filtro a la capa
		var filter = {};
		filter["attribute"]=attribute;
		filter["operation"]=operation;
		filter["value"]=value;
		layer.filters.push(filter);

		var filterList = document.getElementById("filterList");
		var result = renderFilter(filter,layer);
		filterList.appendChild(result);

		// se enceran los controles
		attrs.selectedIndex = 0;
		opers.selectedIndex = 0;
		input.value = '';

		applyFilter(layer,filter);
	});
}

Vue.component("filters_component",{
	template: `
		<div class="modal">
			<div class="modal-content">
				<h4>Filtros</h4>
				<div id="filtersContainer" class="modal-content">
					
				</div>
				<div class="modal-footer">
					<a href="javascript:;" class="modal-action modal-close waves-effect waves-green btn-flat">Cerrar</a>
				</div>
			</div>
		</div>
	`,
	mounted(){
		// se inicializa el modal
		$('.modal').modal();
		// se reacciona al evento
		this.$root.$on('openFilters', function(layer){
			var container = document.getElementById("filtersContainer");
			render(layer,container);
			$('.modal').modal('open');
		});
	}
})

// filtros tiene atributo; operacion; valor
