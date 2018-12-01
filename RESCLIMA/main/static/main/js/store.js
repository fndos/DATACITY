var isEmpty = function(obj){
	for (var prop in obj){
		if (obj.hasOwnProperty(prop))
			return false;
	}
	return true;
};


var store = {
	text:'',
	categories:[],
	bbox:null,
	ini_date:'',
	end_date:'',
	search_option:'layers',
	layers:[],
	series:[],
	// retorna el modelo como un diccionario, 
	// cuyas claves seran los parametros de un query string 
	// de un URL y cuyos valores seran los valores del query string 
	getQueryParams:function(){
		var queryDict = {}
		if(this.text){
			queryDict["text"]=this.text
		}
		var selected_categories_str=""
		for (var i=0;i<this.categories.length; i++){
			var current = this.categories[i]
			if(current["selected"])
				selected_categories_str += current["id"] + ","
		}
		if(selected_categories_str.length>0){
			selected_categories_str = selected_categories_str.slice(0, -1);
			queryDict["categories"]=selected_categories_str
		}
		if(this.bbox!=null){
				var bbox_str  = this.bbox["minX"]+","
				bbox_str += this.bbox["minY"]+","
				bbox_str += this.bbox["maxX"]+","
				bbox_str += this.bbox["maxY"]
				queryDict["bbox"]=bbox_str
			}
		if(this.ini_date!=''){
			queryDict["ini"]=this.ini_date
		}
		if(this.end_date!=''){
			queryDict["end"]=this.end_date
		}
		return queryDict;
		},
	// retorna el modelo como un json
	// que sera usado en un metodo POST
	getPostData:function(){
		var queryDict = {}
		if(this.text!=''){
			queryDict["text"]=this.text;
		}
		var selectedCategories = []
		for(var i=0; i<this.categories.length; i++){
			var category = this.categories[i]
			if(category["selected"]){
				selectedCategories.push(category["name"])
			}
		}
		if(selectedCategories.length>0){
			queryDict["categories"] = selectedCategories
		}
		if(this.bbox){
			queryDict["bbox"] = this.bbox;
		}
		if(this.ini_date!=''){
			queryDict["ini"]=this.ini_date
		}
		if(this.end_date!=''){
			queryDict["end"]=this.end_date
		}
		if(isEmpty(queryDict)){
			return null
		}
		queryDict["option"]=this.search_option
		return queryDict
	},
	getSeriesParams:function(){
		//get the selected series objects inside shared, and form the url to visualize the series
		var selected_series_str="?variables=";
		for (var i=0;i<this.series.length; i++){
			var current = this.series[i];
			if(current["selected"]){
				selected_series_str+=current["variable_id"]+"[";
				iters = current["stations"].length;
				for(var j=0; j<iters; j++){
					if(j!=iters-1){
						selected_series_str+=current["stations"][j]+",";
					}
					else{
						selected_series_str+=current["stations"][j]+"]|";
					}
				}
			}
		}
		selected_series_str = selected_series_str.substring(0, selected_series_str.length - 1);
		if(this.ini_date!=''){
			selected_series_str+="&ini_date="+this.ini_date;
		}
		if(this.end_date!=''){
			selected_series_str+="&end_date="+this.end_date;
		}
		return selected_series_str;
	}
	
}



