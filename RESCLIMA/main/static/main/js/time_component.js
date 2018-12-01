Vue.component("time_component",{
	template: `
		<div class="container">
			<div style="text-align: center">
				<p >Seleccione un rango de fechas</p>
			</div>
			<br>
			<div style="text-align:center">
				<div style="width:150px;display: inline-block;margin-left: 60px">
					<label for="Inicio">Inicio</label>
					<input
					type="date"
					v-bind:value="shared.ini_date"
					v-on:input="updateIniDate($event.target.value)"
					v-bind:max="shared.end_date"/>
				</div>
				<div style="width:150px;display: inline-block;margin-left: 100px">
					<label for="Fin">Fin</label>
					<input
					type="date"
					v-bind:value="shared.end_date"
					v-on:input="updateEndDate($event.target.value)"
					v-bind:min="shared.ini_date"/>
				</div>
			<div>
		</div>
	`,
	mounted(){
		// se obtienen las fechas del url
		var ini_date = this.$route.query["ini"];
		var end_date = this.$route.query["end"];
		var d1=null,d2=null;
		if(ini_date){
			d1 = Date.parse(ini_date);
		}
		if(end_date){
			d2 = Date.parse(end_date);
		}
		// si las dos fechas estan definidas
		if(d1 && d2){
			// se comprueba que fecha ini 
			// sea menor que fecha end
			if(d1>d2){
				return;
			}
		}
		// se setean las fechas en el store de datos global
		if(d1){
			this.shared.ini_date = ini_date;
		}
		if(d2){
			this.shared.end_date = end_date;
		}
		
	},
	data(){
		return {
			shared: store // referencia al store de datos global
		}
	},
	methods:{
		// se ejecuta cuando el usuario ingresa una fecha ini
		updateIniDate(ini_date){
			// se actualiza el store
			this.shared.ini_date = ini_date;
			// se actualiza el url
			var params = this.shared.getQueryParams();
			this.$router.replace({query:params});
		},
		// se ejecuta cuando el usuario ingresa una fecha end
		updateEndDate(end_date){
			// se actualiza el store
			this.shared.end_date = end_date;
			// se actualiza el url
			var params = this.shared.getQueryParams();
			this.$router.replace({query:params});
		}
	}
})

