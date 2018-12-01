// Router
const router = new VueRouter({
  mode: 'history'
})

// app principal
var app = new Vue({
	router,
	el:'#seriesApp',
	data:{
		shared:store
	}
})
