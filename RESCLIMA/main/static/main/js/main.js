// Router
const router = new VueRouter({
  mode: 'history'
})

// app principal
var app = new Vue({
	router,
	el:'#searchForm',
	data:{
		shared:store // referencia al store de datos global
	},
	methods:{
		// cuando se da click en el boton buscar
		// se ejecuta este metodo
		// search(), realiza una peticion post para
		// buscar los resultados (capas o series de tiempo)
		search:function(){
			var option = this.shared.search_option;
			if(option == "layers"){
				this.$root.$emit('searchLayers');
			}
			if(option == "series"){
				this.$root.$emit('searchSeries');
			}
		},

		
	}

})

