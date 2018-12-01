Vue.component("currentlayer_component",{
	template: `
		<div id="currentlayer_component">
			<div class="gradient-45deg-light-blue-cyan" style="padding:10px;color:white">Capa actual</div>
			<div style="padding:10px;">
				<div v-if="shared.currentLayer">
					<div v-if="shared.currentLayer.state=='uninitialized'">
						<div style="width:230px;height:20px;margin:10px;" class="animated-background"></div>
						<div style="width:230px;height:60px;margin:10px;" class="animated-background"></div>
					</div>
					<div v-if="shared.currentLayer.state!='uninitialized'">
						<span>{{shared.currentLayer.title}}</span>
						<div v-if="shared.currentLayer.styles.length>0">
							<div>
								<b>Estilos</b>
								<div class="collection">
									<a  href="#"
									 v-for="style in shared.currentLayer.styles"
									 class="collection-item"
									 v-bind:class="{active:shared.currentLayer.currentStyle.id==style.id}"
									 v-on:click.prevent="changeStyle(style)">
										{{style.title}}
									</div>
								</ul>
							</div>
							<div v-if="shared.currentLayer.currentStyle">
								<b>Leyenda</b>
								<ul>
									<li style="margin-bottom:10px;"
									 v-for="row in shared.currentLayer.currentStyle.legend">
										<strong style="padding:2px 10px;margin:5px;"
										v-bind:style="{'background':row.color}"></strong>
										<span>{{row.label}}</span>
									</li>
								</ul>
							</div>
						</div>
						<div v-else>
							<b>Esta capa no tiene estilos</b>
						</div>
					</div>
				</div>
			</div>
		</div>
	`,
	mounted(){
		
	},
	data(){
		return {
			shared:store,
		}
	},
	methods:{
		// metodo que cambia el estilo de una capa
		changeStyle(style){
			var currentLayer = this.shared.currentLayer;
			var layers = this.shared.layers;
			// si se selecciona el estilo que ya esta
			// seleccionado, no se hace nada
			if(currentLayer.currentStyle == style){
				return;
			}
			// se cambia el estilo de la capa actual
			currentLayer.currentStyle = style;
			this.$forceUpdate();
			// se notifica a los otros componentes
			this.$root.$emit("update_style");
		}
	}
})

