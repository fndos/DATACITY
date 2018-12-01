/*componente que muestra una lista de series de tiempo*/

Vue.component("serielist_component",{
	template: `
		<div>
			<!-- Si el estado del componente es loaded-->
			<!-- muestra la lista de componentes-->
			<!-- serie_component-->
			<div v-if="state=='loaded'">
				<!-- Si hay variables, se muestra la lista -->
				<div v-if="shared.variables.length>0">
			
					<!-- Contenedor de la seriede tiempo --> 
					<!-- de una variable. -->
					<!-- Se itera sobre el array shared.variables -->
					<div v-for="variable in shared.variables">
						<serie_component v-bind:variable="variable"></serie_component>
					</div>
				</div>
				<!--Si no hay series de tiempo se muestra un -->
				<!--mensaje de advertencia -->
				<div v-else>
					<div class="row">
					<div style="text-align:center;margin:100px;">
						<h5><i class="material-icons" style="background:black;color:yellow;">warning</i>
						No hay series de tiempo</h5>
					</div>
				</div>
				</div>
			</div>
			<!-- Si el estado del componente es failed -->
			<!-- se muestra un mensaje de error-->
			<div v-if="state=='failed'">
				<div class="row">
					<div style="text-align:center;margin:100px;">
						<h5><i class="material-icons" style="color:red;">error</i>
						Error en la página. Revise los argumentos del url</h5>
					</div>
				</div>
			</div>
		</div>
	`,
	/*Este metodo se ejecuta cuando se termina de montar
	el template del componente*/
	mounted(){
		/* 
		Se lee el parametro "variables" del queryString
		del  url,  el cual  tiene el siguiente formato:
		variables=id_var1[stacion1,..]|id_var2[stacion1,..]|...|id_varN]

		ese string es parceado y se crea un array de objetos
		con los datos de las variables

		*/

		var variables_str = this.$route.query["variables"];
		var ini_date = this.$route.query["ini_date"]; 
		var end_date = this.$route.query["end_date"];

		if(!ini_date){
			ini_date = null;
		}
		if(!end_date){
			end_date = null;
		}		
		if(!variables_str){
			this.state = "loaded";
			return;
		}

		// colores para asignarle a las estaciones
		// de la variable. Este color sera usado
		// para el color de la linea del trace del plot
		var colors = ['#1f77b4','#ff7f0e','#2ca02c',
					  '#d62728','#9467bd','#8c564b',
					  '#e377c2','#7f7f7f','#bcbd22',
					  '#17becf'];

		//parse data
		var variables_str = variables_str.split("|");
		for(var i=0 ; i < variables_str.length; i++){
			//get the variable id
			var variable_str = variables_str[i];
			var j = variable_str.indexOf("[");
			var k = variable_str.indexOf("]");
			if(j<0 || k<0){
				this.state = "failed";
				return;
			}

			var variable_id = variable_str.slice(0,j);
			var stations_str = variable_str.slice(j+1,k);
			var stations_id = stations_str.split(",");
			
			var variable = {};

			variable["id"]=variable_id;
			variable["name"] = "";
			variable["unit"]="";
			variable["symbol"] = "";
			variable["datatype"]="";
			variable["ini_date"] = ini_date;
			variable["end_date"] = end_date;
			// se crean las estaciones
			variable["stations"] = []
			for(var j=0; j<stations_id.length;j++){
				var station = {}
				station["id"]=stations_id[j]
				station["x_values"]=[];
				station["y_values"]=[];
				station["visible"]=true;
				station["state"]="uninitialized";
				// se obtiene un color
				var color = colors.shift();
				station["color"]=color;
				colors.push(color);
				// se agrega la estacion a la variable
				variable["stations"].push(station);
			}
			variable["state"]="uninitialized";

			// se guarda el objeto en el store
			// compartido
			this.shared.variables.push(variable);
		}
		this.state = 'loaded';

	},
	data(){
		return {
			// estado del componente
			state:'uninitialized',
			// store compartido
			shared:store		
		}
	}
})


