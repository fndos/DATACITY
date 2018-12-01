Vue.component("layers_component",{
	template: `
		<!--Contenedor corredizo, se abre cuando open es True-->
		<div id="layerContainer"
		v-bind:style="[open?{'left':'0px'}:{'left':'-400px'}]">
			
			<!-- Boton que abre y cierra el contenedor-->
			<div id="layerContainerOpen"
			class="gradient-45deg-light-blue-cyan"
			 v-on:click.prevent="open=!open">
				<!-- Dependiendo del valor de open se muestra un icono diferente-->
				<i v-if="open" class="material-icons">keyboard_arrow_down</i>
				<i v-else class="material-icons">keyboard_arrow_up</i>
				Capas
				<!-- Dependiendo del valor de open se muestra un icono diferente-->
				<i v-if="open" class="material-icons">keyboard_arrow_down</i>
				<i v-else class="material-icons">keyboard_arrow_up</i>
			</div>
			<!-- Wrapper-->
			<div id="layerWrapper">
				<!-- Menu con opciones de las capas-->
				<div class="positionMenu">
					<div class="positionBtn"
					 v-on:click.prevent="moveLayer(-1)">
						<i class="material-icons">keyboard_arrow_up</i>
					</div>
					<div class="positionBtn"
					 v-on:click.prevent="moveLayer(1)">
						<i class="material-icons">keyboard_arrow_down</i>
					</div>
				</div>
				<!-- Contenedor con la lista de capas -->
				<div id="layerList" >
					<!-- Si hay capas en shared.layers se muestra la lista-->
					<div v-if="shared.layers.length>0">
						<!-- Contenedor de la capa -->
						<!-- se intera sobre el array shared.layers -->
						<!-- Si la capa es igual a currentLayer, se pinta-->
						<div v-for="layer in shared.layers"
						class="layerItem"
						v-bind:style="[shared.currentLayer.id==layer.id?{'background':'#EFEBE9'}:{}]">
							<!-- Si la capa tiene estado uninitialized-->
							<!-- Se muestran animaciones-->
							<div v-if="layer.state=='uninitialized'">
								<div style="width:100px;height:20px;margin:10px;" class="animated-background"></div>
								<div style="width:200px;height:20px;margin:10px;" class="animated-background"></div>
								<div style="width:20px;height:20px;margin:10px;" class="animated-background"></div>
							</div>
							<!-- Si la capa tiene estado distinto a uninitialized-->
							<!-- Se muestran los metadatos de la capa -->
							<div v-if="layer.state!='uninitialized'">
								<!-- Opcion zoom a la capa-->
								<div style="height:100%;position: relative;">
									<div style="position:absolute;right:10px;">
										<span title="Zoom a la capa"
										  class="layerBtn"
										  v-on:click.prevent="zoomToLayer(layer)">
											<i class="material-icons">zoom_in</i>
										</span>
										<!--
										<span title="Filtros"
										 class="layerBtn" 
										 v-if="layer.type=='vector'"
										 v-on:click.prevent="openFilters(layer)">
											<i class="material-icons">filter_list</i>
										</span>-->
									</div>
								</div>

								<!-- El titulo de la capa-->
								<!-- Si se da click es esta capa, se convierte en-->
								<!-- currentLayer -->
								<h5 class="header layerTitle"
								 v-on:click.prevent="shared.currentLayer=layer">
									{{layer.title}}
								</h5>
								<!-- El resumen de la capa -->
								<p>{{layer.abstract}}</p>
								<!-- La fecha de la capa-->
								<h6>{{layer.data_date}}</h6>

								<!-- Contenedor con opciones de la capa -->
								<!-- Solo se muestra si el estado de la capa es loaded-->
								<div class="layerOptions" v-if="layer.state=='loaded'">
									<!-- Slider para controlar la transparencia-->
									<p class="range-field">
										<label>Transparencia</label>
										<input type="range" 
										min="0" 
										max="100" 
										value="0"
										v-model="layer.opacity"
										v-on:input="changeOpacity(layer)"/>
									</p>
									<!-- Links para descargar y remover la capa-->
									<div>
										<a style="padding:10px;color:green" v-bind:href="downloadLink(layer)">
											<i class="material-icons">file_download</i>Descargar
										</a>
										<a style="padding:10px;color:red" href="#!" v-on:click.prevent="removeLayer(layer)">
											<i class="material-icons">delete</i>Eliminar
										</a>
									</div>
								</div>
								<!-- Si la capa no tiene estado loaded-->
								<!-- no se muestran las opciones de la capa,-->
								<!-- se muestra una animacion-->
								<div v-else>
									<div class="animated-background" style="height:80px">Cargando...</div>
								</div>
							</div>
						</div>
					</div>
					<!-- Si no hay capas en shared.layers se muestra un mensaje-->
					<div v-else>
						<p>No hay capas</p>
					</div>
				</div>
			</div>
		</div>
	`,
	mounted(){
		/*Se posiciona correctamente el elemento*/
		var elements = document.getElementsByClassName("navbar-fixed");
		var navbar = elements[0];
		var height = navbar.getBoundingClientRect()["height"];
		height = Math.ceil(height);
		layerContainer.style.top = String(height) + "px";

		/* Se lee el parametro "layers" del queryString
		del url, el cual tiene el siguiente formato:
		layers=id_capa1|id_capa2|...|id_capaN */
		var query_string = this.$route.query["layers"];
		if (!query_string){
			return;
		}
		// se obtienen los ids de las capas
		var layer_ids = query_string.split("|");
		// se crean objetos que representan las capas
		for(var i=0; i<layer_ids.length; i++){
			var id_layer = layer_ids[i];
			// Si el string es vacio, no se hace nada
			if(!id_layer){
				return;
			}
			var layer = {};
			layer["id"]=id_layer;
			layer["index"]=i;
			layer["state"]="uninitialized";
			layer["title"]="";
			layer["abstract"]="";
			layer["type"]="";
			layer["data_date"]="";
			layer["opacity"]=0;
			layer["styles"]=[];
			layer["filters"]=[];
			// se guarda el objeto en el store
			// compartido
			this.shared.layers.push(layer);
			// se piden los metadatos de la capa
			this.getLayerInfo(layer);
		}
		// se selecciona la capa actual (currentLayer)
		// es la primera capa
		if(layer_ids.length>0){
			var currentLayer = this.shared.layers[0];
			this.shared.currentLayer=currentLayer;
		}
	},
	data(){
		return {
			shared:store,
			open:true,
		}
	},
	methods:{
		/*Metodo que realiza una peticion ajax
		para obtener los metadatos de la capa*/
		getLayerInfo(layer){
			var id_layer = layer["id"];
			var index = layer["index"];
			
			var url = "/layer/info/"+id_layer
			// referencia al componente
			var self = this;
			// peticion GET
			var request = $.get(url);
			request.done(function(data){
				layer["title"]=data["title"]
				layer["abstract"]=data["abstract"]
				layer["type"]=data["type"];
				layer["data_date"]=data["data_date"];
				layer["bbox"]=data["bbox"];
				// se actualiza el estado de la capa
				layer["state"]="metadata_loaded"
				// se agregan los estilos
				var styles = data["styles"]
				for(var i=0; i<styles.length; i++){
					var style = styles[i]
					// los estilos aun no tienen legenda
					// se agrega un array vacio
					style["legend"]=[];
					layer["styles"].push(style);
				}
				// se selecciona el primer estilo
				// como currentStyle de la capa
				if (layer["styles"].length>0){
					var style = layer["styles"][0];
					layer["currentStyle"]=style;
				}
				// se notifica a los otros componentes
				// que la capa ya tiene metadatos
				self.$root.$emit("layer_metadata",layer);
			});
		},
		/*
		Metodo para actualizar la transparencia
		de una capa
		*/
		changeOpacity(layer){
			var opacity = layer["opacity"];
			var openlayer_layer = layer["openlayer_layer"];
			openlayer_layer.setOpacity(1-opacity/100);
		},
		/*
		Metodo para realizar un zoom a la capa
		*/
		zoomToLayer(layer){
			var extent = layer["extent"];
			if(extent){
				var map = this.shared.map;
				map.zoomToExtent(extent);
			}
		},
		moveLayer(direction){
			var layers = this.shared.layers;
			var currentLayer = this.shared.currentLayer;
			var ini = currentLayer["index"];
			var end = ini + direction;
			var limit = layers.length - 1;
			if(end<0 || end > limit ){
				return;
			}
			layers.splice(ini,1);
			layers.splice(end,0,currentLayer);
			// actualizar los index
			currentLayer["index"]=end;
			currentLayer["openlayer_layer"]
			var changedLayer = layers[ini];
			changedLayer["index"]=ini;
			// actualizar los zIndex
			var zIndex1 = currentLayer["openlayer_layer"].getZIndex()
			var zIndex2 = changedLayer["openlayer_layer"].getZIndex()
			currentLayer["openlayer_layer"].setZIndex(zIndex2);
			changedLayer["openlayer_layer"].setZIndex(zIndex1);

		},
		openFilters(layer){
			this.$root.$emit("openFilters",layer);
		},
		downloadLink(layer){
			if(layer.type=="vector"){
				return "/vector/export/"+layer.id;
			}
			else if(layer.type=="raster"){
				return "/raster/export/"+layer.id;
			}
			else{
				return "#!"
			}
		},
		removeLayer(removing_layer){
			var index = removing_layer.index;
			var layers = this.shared.layers;
			// se elimina la capa de la lista 
			// de capas
			layers.splice(index,1);

			var numLayers = layers.length;

			// se actualizan los index y z-index
			// de las otras capas
			for(var i=0;i<numLayers;i++){
				var layer = layers[i];
				layer.index = i;
				layer.zIndex = numLayers - index;
				layer.openlayer_layer.setZIndex(layer.zIndex)
			}
			// se remueve el capa del mapa de openlayers
			var map = this.shared.map;
			map.removeLayer(removing_layer.openlayer_layer,false);
			removing_layer.openlayer_layer.destroy();

			if(layers.length>0){
				this.shared.currentLayer = layers[0];
			}else{
				this.shared.currentLayer = null;
			}
		}
	}
})

