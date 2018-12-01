// componente del bbox

Vue.component("bbox_component",{
	template: `
		<div class="row">
			<div class="col s1">
			</div>
			<div class="col s10">
				<div id="bbox_container" style="text-align:center;"></div>
			</div>
			<div class="col s1">
			</div>
		</div>
	`,
	mounted(){
		// se inicializa el objeto BboxSelector,
		// recibe un callback cuando actualiza el bbox
		bboxSelector = new BboxSelector("bbox_container",this.setBBox)
		// se obtiene el bbox del url
		var bbox_string = this.$route.query["bbox"];
		// si hay bbox en el url, se actualiza el bbox
		// global
		if(bbox_string){
			var bbox_data = bbox_string.split(",");
			var left = parseFloat(bbox_data[0]);
			var bottom = parseFloat(bbox_data[1]);
			var rigth = parseFloat(bbox_data[2]);
			var top = parseFloat(bbox_data[3]);
			// los tres valores deben estar definidos
			if(!left || !bottom || !rigth || !top){
				return;
			}
			// se valida el rango de valores
			if(left < -180 || left > 180){
				return;
			} 
		 	if(rigth < -180 || rigth > 180){ 
		 		return;
			}
 			if(bottom < -90 || bottom > 90){ 
 				return;
			}
			if(top < -90 || top > 90){
				return;
			}
			// se valida si el bbox es valido
			if(left > rigth){
				return;
			}
			if(bottom > top){
				return;
			}
						
			// se setea el bbox en el selector
			bboxSelector.setBBox(left,bottom, rigth, top);
			// se crea el bbox del store de datos
			bbox = {}
			bbox["minX"] = left;
			bbox["minY"] = bottom;
			bbox["maxX"] = rigth;
			bbox["maxY"] = top;
			this.shared.bbox = bbox
		}
	},
	data(){
		return{
			bboxSelector: null,
			shared:store
		}
	},
	methods:{
		// callback que se llama cuando bboxSelector, 
		// actualiza el bbox
		setBBox(bbox){
			if(bbox==null){
				this.shared.bbox = null
			}
			else{
				this.shared.bbox = {};
				this.shared.bbox["minX"] = bbox.left;
				this.shared.bbox["minY"] = bbox.bottom;    
				this.shared.bbox["maxX"] = bbox.right;
				this.shared.bbox["maxY"] = bbox.top;
			}
			// actualiza el url
			var params = this.shared.getQueryParams();
			this.$router.replace({query:params});
		}
	}

})

