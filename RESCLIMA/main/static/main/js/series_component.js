Vue.component("series_component",{
	// este componente debe reaccionar al arreglo de resultados
	// this.shared.series

	//PONER COMO DESCRIPCION NUMERO DE ESTACIONES
	
	template: `
		<div>
			<!-- si el estado de las series es searched se -->
			<!-- muestran los resultados -->
			<div v-if="state=='searched'">
				<div v-if="shared.series.length > 0">
					<div>
						<a
						class="btn waves-effect waves-light gradient-45deg-light-blue-cyan" 
						v-bind:disabled="selected_count==0"
						v-on:click="visualizeSeries">
							<i class="material-icons left">remove_red_eye</i>Visualizar</a>
						<a
						class="btn waves-effect waves-light gradient-45deg-light-blue-cyan" 
						v-bind:disabled="selected_count==0"
						v-on:click="downloadSeries">
							<i class="material-icons left">file_download</i>Descargar</a>
					</div>
					<div v-for="serie in shared.series">
						<div class="card">
							<div class="card-content">
								<span class="card-title">
									<input
									type="checkbox"
									v-bind:id="serie.variable_id"
									v-bind:value="serie.selected"
									v-on:input="selectSerie(serie)">
									<label v-bind:for="serie.variable_id"></label>
									{{serie.variable_name}}
								</span>
								<p>Se han encontrado {{serie.stations.length}} estaciones en la búsqueda.</p>
							</div>
						</div>		
					</div>
					<!-- botones de paginacion -->
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
				<div v-else>No hay resultados</div>
			</div>
			<!-- si el estado de las series es loading se -->
			<!-- muestra una animacion -->
			<div v-if="state=='loading'">
				<div class="preloader-wrapper big active">
					<div class="spinner-layer spinner-blue-only">
						<div class="circle-clipper left">
							<div class="circle"></div>
						</div>
						<div class="gap-patch">
							<div class="circle"></div>
						</div>
						<div class="circle-clipper right">
							<div class="circle"></div>
						</div>
					</div>
				</div>
			</div>
			<!-- si el estado de las series es fail se -->
			<!-- muestra un mensaje de error -->
			<div v-if="state=='fail'">
				<div class="red">
					<b>Ha ocurrido un error</b>
				</div>
			</div>
		</div>				
	`,
	data(){
		return {
			selected_count:0,
			state:'initial',
			// limit y offset controlan la paginacion
			limit:4,
			offset:0,
			// maximo offset, al principio
			// se tiene un valor negativo
			max_offset:-1,
			shared:store
		}
	},
	mounted(){
		this.$root.$on('searchSeries', this.searchSeries);
	},
	methods:{
		searchSeries(){
			// se obtienen los parametros de busqueda
			var data = this.shared.getPostData()
			if(data==null){
				return;
			}
			// referencia al componente
			var self = this;
			var url = "search/series/";
			// se agrega el limit y el offset
			data["limit"] = self.limit;
			data["offset"] = self.offset;
			// se realiza la peticion ajax
			data = JSON.stringify(data);
			var request = $.post(url,data);
			self.state = "loading";	
			request.done(function(response){
				var  results = response["series"];
				// se determina el maximo offset
				var full_count = response["full_count"];
				var max_offset = full_count - self.limit;

				if(max_offset>0){
					self.max_offset = max_offset;
				}else{
					self.max_offset = 0;
				}

				// se copian los resultados en el
				// array layers
				var series = self.shared.series;
				series.splice(0, series.length);
				for (var i=0;i< results.length; i++){
					series.push(results[i]);
				}
				// se cambia el estado
				self.state = "searched";
			});
			request.fail(function(error){
				self.state = "fail";	
			});

		},
		selectSerie(serie){
			serie.selected = !serie.selected;
			if(serie.selected==true) 
				this.selected_count +=1;
			if(serie.selected==false)
				this.selected_count -=1;
		},
		visualizeSeries(){
			//redirect to the url to visualize the selected time series
			var url = "series/view/" + this.shared.getSeriesParams();
			//this.$router.replace(url);
			//this.$router.go();
			url = encodeURI(url)
			window.open(url,'_blank');
		},
		createDownloadLink(serie){
			var url = "/series/measurements/download/?variable="
			var variable_str = serie.variable_id + "["
			var length = serie.stations.length - 1;
			for(var i=0;i< length;i++){
				var station = serie.stations[i];
				variable_str += station + "," 
			}
			var station = serie.stations[length];
			variable_str += station + "]"
			url += variable_str;

			if(this.shared.ini_date){
				url = url + "&ini_date=" + this.shared.ini_date;
			}
			if(this.shared.end_date){
				url = url + "&end_date=" + this.shared.end_date;
			}
			
			return url;
		},
		downloadSeries(){
			// se iteran todas las capas seleccionadas
			for(var i=0; i<this.shared.series.length; i++){
				var serie = this.shared.series[i];
				if (serie["selected"]){
					var url = this.createDownloadLink(serie)
					var link = document.createElement("a");
					link.style.display = 'none';
					document.body.appendChild(link);
					link.setAttribute('download',"serie_"+serie["id"]);
					link.href = url;
					link.click();
					document.body.removeChild(link);
				}
			}
		},
		prev(){
			if(this.offset <= 0){
				return;
			}
			this.offset -= this.limit;
			this.searchSeries();
		},
		next(){
			if(this.offset>=this.max_offset){
				return;
			}
			this.offset += this.limit;
			this.searchSeries();
		}
		
	}
})

