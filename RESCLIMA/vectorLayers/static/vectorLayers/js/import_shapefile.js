

// renderiza el progreso del procesamiento
// de la capa
function renderProcess(task_id){
	$.ajax({
		type: 'get',
		url: '/get-task-info/',
		data: {'task_id': task_id},
		success: function (data) {
			// recibe un objeto 
			// data{"result":{"percent":porcentaje,"error":"mensaje de error"}
			// ,"state":estado del task}

			if(data["result"]["error"]){
				renderError(data["result"]["error"]);
				return;
			}

			// se hace visible la barra
			// de progreso
			var progressContainer = document.getElementById("progress-container");
			progressContainer.style.visibility = "visible";

			// si el estado de la tarea en celery
			// es PENDING. Se muestra un mensaje: Procesando 0%
			if (data.state == 'PENDING') {
				uploadPercent.style.width = "0%";
				uploadPercentLabel.innerText = "Procesando 0%";
			}
			// Si el estado de la tarea en Celery es PROGRESS o SUCCESS
			// se muestra el progreso actual en la barra
			else if (data.state == 'PROGRESS' || data.state == 'SUCCESS') {
				var percentComplete_str = data.result.percent.toFixed(2) + "%"
				uploadPercent.style.width = percentComplete_str;
				uploadPercentLabel.innerText = "Procesando "+percentComplete_str;
			}
			
			// Si el estado es SUCCESS, se redirije a /vector/
			if(data.state == 'SUCCESS'){
				document.location.href = "/vector/"
			}
			// si el estado es diferente de SUCCESS
			// se vuelve  a pedir informacion de la tarea de Celery 
			if (data.state != 'SUCCESS') {
				setTimeout(function () {
					renderProcess(task_id)
				}, 100);
			}
		},
		error: function (data) {
			var error_msg = "Error " + data.error;
			renderError(error_msg);
		}
	});
}


function renderError(error){
	errorMsg.innerHTML = '<div class="red"><b>' + error + '</b></div>'
	var progressContainer = document.getElementById("progress-container");
	progressContainer.style.visibility = "hidden";
	window.scrollTo(0, 0);
	// se activa el boton cancelar
	var cancelButton = document.getElementById("Cancel");
	cancelButton.disabled = false;
}

// crea un objeto xmlhttprequest 
// con el evento upload.progress
function createXHR(){
	var xhr = new window.XMLHttpRequest();
	
	// este evento mostrara el progreso de la subida
	// de los datos
	xhr.upload.addEventListener("progress",function(evt){
	if (evt.lengthComputable){
		// hace visible el contenedor de la barra de progreso
		var progressContainer = document.getElementById("progress-container");
		progressContainer.style.visibility = "visible";
		var percentComplete = evt.loaded / evt.total;
		percentComplete = parseInt(percentComplete * 100);
		var percentComplete_str = String(percentComplete) + "%"
		uploadPercent.style.width = percentComplete_str;
		if (percentComplete === 100){
			uploadPercentLabel.innerText = "Completado, espere por favor";
			return;
		}
		uploadPercentLabel.innerText = "Subiendo " + percentComplete_str;
	}
	},false);
	return xhr;
}


// se ejecuta cuando la subida de los datos
// es exitosa
function successHandler(data){
	
	// recibe un objeto 
	//data{"error":"mensaje de error","task_id":id del task}

	// si no hay error se muestra el
	// porcentaje de procesamiento
	if(!data.error){
		renderProcess(data.task_id);
	}// si hay un error se muestra
	else{
		// pendiente mejora aspecto del error
		renderError(data.error);
	}
}

// se ejecuta si ocurre un error en la subida del form
function errorHandler(data){
	status = String(data.status);
	msg = "Ha ocurrido un error " + status+ " en el servidor"
	renderError(msg);
}

// obtiene el string de categorias
function getCategoriesString(){
	categories_string = "";
	nodes = document.querySelectorAll("#categories .selected");
	for(var i=0; i<nodes.length; i++){
		var node = nodes[i];
		categories_string += node.innerText + " ";
	}
	categories_string = categories_string.slice(0, -1);
	return categories_string;
}

// revisa las condiciones de los
// archivos
function checkFiles(){
	var file_input = document.getElementById("id_import_files");
	var list_files = file_input.files;

	var required_extensions = ["shp", "shx", "dbf", "prj"];
	var has_extension = {};
	for(var i=0; i<required_extensions.length; i++){
		var extension = required_extensions[i];
		has_extension[extension] = false
	}
	filename = null;
	for(var i=0; i<list_files.length; i++){
		var f = list_files[i];
		var parts = f.name.split(".");
		if(parts.length!=2){
			return "Los archivos deben tener extension ni contener puntos en el nombre" 
		}
		// se obtiene el nombre y extension del archivo
		var fname = parts[0].toLowerCase();
		var extension = parts[1].toLowerCase();
		// se comprueba que todos los archivos se llamen igual
		if(filename==null){
			filename = fname
		}
		else if(filename!=fname){
			return "Todos los archivos deben tener el mismo nombre";
		}

		if (required_extensions.includes(extension)){
			has_extension[extension] = true;
		}
		else{
			return "No se admite archivo con extension " + extension;
		}
	}
	// se valida que los archivos requeridos existan
	for(var i=0; i<required_extensions.length; i++){
		var extension = required_extensions[i];
		if(!has_extension[extension]){
			return "Archivo perdido requerido ."+extension
		}
	}
	return null;

}


// se ejecuta cuando se da click en una categoria
function markCategory(event){
	var category = event.target;
	var classCategory = category.className;
	if(classCategory.indexOf("selected") !== -1){
		category.className = "chip z-depth-3"
	}else{
		category.className = "chip z-depth-3 cyan selected"
	}
}

// se ejecuta cuando se hace submit
// al form
function formSubmit(e){
	e.preventDefault(e);
	
	var formImport = $("#shapefileForm");
	// se obtiene los datos del formulario
	var data = new FormData(formImport.get(0));
	// se obtiene el string de categorias
	var categories_string = getCategoriesString();
	data.append("categories_string",categories_string);

	// se checkean las condiciones de los archivos
	var result = checkFiles();
	if(result){
		renderError(result);
		return;
	}

	// se desactiva el boton cancelar
	var cancelButton = document.getElementById("Cancel");
	cancelButton.disabled = true;

	// se envian los datos al servidor
	$.ajax({
		type: formImport.attr('method'),
		url: formImport.attr('action'),
		data: data,
		processData: false,
		contentType: false,
		xhr: createXHR,
		success: successHandler,
		error: errorHandler
	});
	return false;
}

$(document).ready(function() {
	document.getElementById('data_date').valueAsDate = new Date();
	var formImport = $("#shapefileForm");
	formImport.submit(formSubmit);
});



