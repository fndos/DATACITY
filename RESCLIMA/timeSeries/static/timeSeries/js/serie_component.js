Vue.component("serie_component",{
	template: `
		<!--Contenedor del component -->
		<div>
			<!-- Si el estado de la variable es failed-->
			<!-- se muestra un mensaje de error-->
			<div class="card"
			 v-bind:style="[variable.state=='failed'?{'display':''}:{'display':'none'}]" >
				<div class="row">
					<div style="text-align:center;margin:100px;">
						<h5><i class="material-icons" style="color:red;">error</i>
						Error en la variable</h5>
					</div>
				</div>
			</div>
			<!-- Si el estado es diferente de failed-->
			<!-- se muestra la variable-->
			<div class="card"
			 v-bind:style="[variable.state!='failed'?{'display':''}:{'display':'none'}]">
				<!-- si el estado es uninitialized -->
				<!-- se muestra una animacion -->
				<div v-bind:style="[variable.state=='uninitialized'?{'display':''}:{'display':'none'}]">
					<div class="card-header cyan accent-4">
						<div class="card-title white-text">
							 <h4 class="card-title">Cargando...</h4>
						</div>
					</div>
					<div class="card-content">
						<div style="width:100%;height:500px;margin:10px;" class="animated-background"></div>
					</div>
				</div>
						
				<!-- Si la variable tiene estado loaded-->
				<!-- Se muestran los metadatos de la variable -->
				<div v-bind:style="[variable.state=='loaded'?{'display':''}:{'display':'none'}]">
					<nav class="nav-wrapper cyan accent-4">
						<ul class="left"><li><h1 class="logo-wrapper">
							<a href="#!">
								<span class="logo-text">{{variable.name}} vs tiempo</span>
							</a>
						</h1></li></ul>
						<ul class="right"><li>
							<a v-bind:href="downloadLink" title="Descargar">
								<i class="material-icons">file_download</i>
							</a>
						</li></ul>
					</nav>
					<div class="card-content">
						<!-- Solo se muestra si el tipo de dato de la-->
						<!-- variable es float-->
						<div v-bind:style="[variable.datatype=='float'?{'display':''}:{'display':'none'}]">
							<!-- Contenedor para el plot y la leyenda-->
							<div class="row">
								<div class="col s10">
									<!-- Contenedor para el plot -->
									<div v-bind:data-plot-id="variable.id"></div>
								</div>
								<div class="col s2">
									<!-- Contenedor para la leyenda -->
									<div>
										<div v-for="station in variable.stations">
											<!-- Si la estacion tiene estado loading -->
											<!-- se muestra una animacion -->
											<div v-if="station.state == 'loading'">
												<div style="width:100px;height:20px;margin:10px;" class="animated-background"></div>
											</div>
											<!-- Si la estacion tiene estado failed -->
											<!-- Se muestra un mensaje de error-->
											<div v-if="station.state == 'failed'">
												<i class="material-icons" style="color:red;">error</i>
												<span style="opacity:0.5;color:red;">{{"Estación " + station.id}}</span>
											</div>
											<!--Si la traza de la estacion esta cargada -->
											<!-- se muestra el legend item -->
											<div class="legendItem"
											 v-if="station.state == 'loaded'"
											 v-bind:style="[station.visible?{'opacity':'1'}:{'opacity':'0.5'}]"
											 v-on:click.prevent="showHideTrace(station)">
												<strong class="legendSymbol"
													v-bind:style="{'background':station.color}">
												</strong>
												<span>{{"Estación " + station.id}}</span>
											</div>
										</div>
									</div>
								</div>
							</div>						
							<!-- botones de paginacion -->
							<!-- Si hay mas datos que mostrar, se muestran los botones-->
							<div class="row"
								v-if="offset != 0 || offset < max_offset">
								<ul class="pagination">
									<li v-bind:class="{disabled: offset == 0}"
									    v-on:click.prevent="prev()">
										<a href="#!">
											<i class="material-icons">chevron_left</i>
										</a>
									</li>
									<li v-bind:class="{disabled: offset >= max_offset}"
									    v-on:click.prevent="next()">
										<a href="#!">
											<i class="material-icons">chevron_right</i>
										</a>
									</li>
								</ul>
							</div>
						</div>
						<!-- Si el tipo de dato de la variable no es float-->
						<!-- se muestra un mensaje de warning-->
						<div class="row"
						 v-bind:style="[variable.datatype!='float'?{'display':''}:{'display':'none'}]">
							<div style="text-align:center;margin:100px;">
								<h5><i class="material-icons" style="background:black;color:yellow;">warning</i>
								No se puede visualizar el tipo de datos {{variable.datatype}}</h5>
							</div>
						</div>
					</div>
				</div>	
			</div>
		</div>
	`,
	props:["variable"],
	mounted(){
		var variable = this.variable;
		var id_variable = variable.id;
		// se obtiene el contenedor del plot
		var nodes = document.querySelectorAll('[data-plot-id="'+id_variable+'"]');
		if(nodes.length==0){
			console.log("lo hago failed en mounted",variable)
			variable.state = "failed";
			return;
		}
		this.container = nodes[0];
		// se obtiene la informacion de las variables
		this.getVariableInfo(variable);
	},

	data(){
		return {
			// referencia al contenedor del plot
			container:null,
			// variable para la paginacion
			limit:100,
			offset:0,
			max_offset:-1,
			shared:store,
		}
	},
	computed:{
		// crea el link de descarga de datos
		downloadLink:function(){
			var url = "/series/measurements/download/?variable="
			var variable = this.variable;
			var variable_str = variable.id + "["
			var length = variable.stations.length - 1;
			for(var i=0;i< length;i++){
				var station = variable.stations[i];
				variable_str += station.id + "," 
			}
			var station = variable.stations[length];
			variable_str += station.id + "]"
			url += variable_str;

			if(variable["ini_date"]){
				url = url + "&ini_date=" + variable["ini_date"];
			}
			if(variable["end_date"]){
				url = url + "&end_date=" + variable["end_date"];
			}
			
			return url;
		}
	},
	methods:{
		/*
		Realiza una peticion ajax para 
		obetenr los metadados de una variable*/
		getVariableInfo(variable){
			var url = "/series/variable/info/"+variable.id;
			var request = $.get(url);
			var self = this;
			request.done(function(data){
				variable["name"]=data["name"];
				variable["unit"]=data["unit"];
				variable["symbol"]=data["symbol"];
				variable["datatype"]= data["datatype"];
				variable["state"]="loaded";
				// se inicializa el plot
				self.initializePlot(variable);
				// se piden los datos solo si el tipo de 
				// dato es float
				if(variable["datatype"]=="float"){
					self.getMeasurements(variable);	
				}
				
			});
			request.fail(function(data){
				console.log("lo hago failed",variable);
				variable.state = 'failed';
			});
		},
		/*
		Por cada estacion de la variable,
		pide los datos de la estacion
		*/
		getMeasurements(variable){
			var stations = variable["stations"];
			for(var i=0; i<stations.length; i++){
				var station = stations[i];
				this.getStationMeasurements(variable,station);
			}
		},
		/*
		Pide la serie de tiempo de una estacion.
		*/
		getStationMeasurements(variable,station){
			var self = this;
			// se crea el url			
			var url = "/series/measurements/?";
			url += "variable_id="+variable["id"];
			url += "&station_id="+station["id"];
			if(variable["ini_date"]){
				url +="&ini_date="+variable["ini_date"];
			}
			if(variable["end_date"]){
				url +="&end_date="+variable["end_date"];
			}
			url+="&limit="+this.limit;
			url+="&offset="+this.offset;

			var request = $.get(url);
			station["state"]="loading";
			request.done(function(response){
				var measurements = response["measurements"];
				// se actualiza
				var full_count = response["full_count"];
				self.max_offset = full_count - self.limit;
				
				self.assingMeasurements(station,measurements);
				// dibuja el plot
				self.addTrace(variable,station);
			});
			request.fail(function(response){
				station["state"]="failed";
			});
		},
		/*
		Asigna la serie de tiempo a la estacion
		*/
		assingMeasurements(station,measurements){
			station["x_values"] = [];
			station["y_values"] = [];
			for(var i=0;i<measurements.length; i++){
				var m = measurements[i];
				station["x_values"].push(m["ts"]);
				station["y_values"].push(m["value"]);
			}
			station["state"]="loaded";
		},
		/*
		Inicializa el plot usando la libreria Plotly
		*/
		initializePlot(variable){
			var data = []
			var y_title = variable["unit"]+ " ( " + variable["symbol"] + " )";
			var layout = {
				showlegend: false,
				autosize:true,
				margin: {
					l: 50,
					r: 10,
					b: 50,
					t: 50,
					pad: 4
				},
				yaxis:{title: y_title}
			};
			Plotly.newPlot(this.container,data,layout,{responsive: true});
			// se actualiza el plot
			Plotly.Plots.resize(this.container);
		},
		/*
		Agrega una traza al plot
		*/
		addTrace(variable,station){
			var container = this.container;
			var data = container.data;
			var n_traces = data.length;

			station["trace_index"]=n_traces;
			// se crea el trace
			var trace = {
				x:station["x_values"],
				y:station["y_values"],
				type: 'scatter',
				name: 'Estacion '+station["id"],
				line:{color:station["color"]},
				visible:station["visible"]
			};
			Plotly.addTraces(container,[trace]);
		},
		/*
		Muestra u oculta una traza del plot,
		dependiendo del valor de verdad del
		atributo "visible" de la estacion
		*/
		showHideTrace(station){
			station["visible"]=!station["visible"];
			var container = this.container;
			var data = container.data;
			var trace_index = station["trace_index"];
			var trace = data[trace_index];
			trace.visible = station["visible"];
			Plotly.redraw(container);
		},
		/*
		Handler del boton prev, en la
		paginacion. Trae los anteriores datos
		*/
		prev(){
			if(this.offset <= 0){
				return;
			}
			this.offset -= this.limit;
			var container = this.container;
			var variable = this.variable;
			this.initializePlot(variable);
			this.getMeasurements(variable);
		},
		/*
		Handler del boton next, en la
		paginacion. Trae los siguiente datos
		*/
		next(){
			if(this.offset>=this.max_offset){
				return;
			}
			this.offset += this.limit;
			var container = this.container;
			var variable = this.variable;
			this.initializePlot(variable);
			this.getMeasurements(variable);
		}
	}
})

