// ******************************************************************
// ************************* Simple function ************************
// ******************************************************************

function toTitleCase(str) {
    return str.replace(/\w\S*/g, function(txt){
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
}

function getPieChartPluginSize(str) {
  return parseInt(str[str.length-1]);
}

function getPieChartViewBox(size) {
	if (size == 4) { return "-152 0 712 712" }
	else if (size == 5) { return "-152 0 685 685" }
	else if (size == 6) { return "-152 0 675 675" }
	else { return "-152 0 675 675" }
}

function isEmpty(str) {
	if (!str) { return true; }
	else { return false }
}

function d3PieChartSample(container, source, date, size) {
  if (isEmpty(date)) {
    // Una de las fechas ingresadas no es valida
    date = null;
  }

  var colorScheme = ["#FF8A65", "#4DB6AC","#FFF176","#BA68C8","#00E676","#AED581","#9575CD","#7986CB","#E57373","#A1887F","#90A4AE","#64B5F6"];

  var margin = {top:50,bottom:50,left:50,right:50};
	var width = 500 - margin.left - margin.right, height = width, radius = Math.min(width, height) / 2;
	var donutWidth = 75;
	var legendRectSize = 16;
	var legendSpacing = 4;

  d3.json("http://127.0.0.1:8000/api/" + source + "/" + date + "/" , function(error, data) {
    data.forEach(function(item){
  		item.enabled = true;
  	});

  	var color = d3.scale.ordinal().range(colorScheme);

  	var svg = d3.select(container)
      .append("svg")
      .attr("viewBox", getPieChartViewBox(getPieChartPluginSize(size)))
  	  .attr("perserveAspectRatio", "xMinYMid")
      .append("g")
    	.attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

  	var arc = d3.svg.arc()
  	  .outerRadius(radius - 10)
      .innerRadius(radius - donutWidth);

  	var pie = d3.layout.pie()
  		.sort(null)
  		.value(function(d) { return d.value; });

  	var tooltip = d3.select(container)
  		.append('div')
  		.attr('class', 'tooltip');

  	tooltip.append('div')
  		.attr('class', 'tip-label');

  	tooltip.append('div')
  		.attr('class', 'count');

  	tooltip.append('div')
  		.attr('class', 'percent');

  	var path = svg.selectAll('path')
  		.data(pie(data))
  		.enter()
  		.append('path')
  		.attr('d', arc)
  		.attr('fill', function(d, i) {
  			return color(d.data.key);
  		})
  		.each(function(d) { this._current = d; });

  	path.on('mouseover', function(d) {
  		var total = d3.sum(data.map(function(d) {
  			return (d.enabled) ? d.value : 0;
  		}));

			tooltip.select('.tip-label').html(d.data.key);
			tooltip.select('.count').html(d.data.data);
			tooltip.select('.percent').html(d.data.value + '%');

			tooltip.style('display', 'block');
			tooltip.style('opacity',2);

  	});

  	path.on('mousemove', function(d) {
  		tooltip.style('top', (d3.event.layerY + 10) + 'px')
  		.style('left', (d3.event.layerX - 25) + 'px');
  	});

  	path.on('mouseout', function() {
  		tooltip.style('display', 'none');
  		tooltip.style('opacity',0);
  	});

  	var legend = svg.selectAll('.legend')
  	  .data(color.domain())
  	  .enter()
  	  .append('g')
      .attr('class', 'legend')
      .attr('transform', function(d, i) {
  	    var height = legendRectSize + legendSpacing;
        var offset =  height * color.domain().length / 2;
        var horz = -2 * legendRectSize;
        var vert = i * height - offset;
        return 'translate(' + horz + ',' + vert + ')';
  	});

  	legend.append('rect')
  		.attr('width', legendRectSize)
  		.attr('height', legendRectSize)
  		.style('fill', color)
  		.style('stroke', color)
  		.on('click', function(label) {
  	    var rect = d3.select(this);
  		 	var enabled = true;
  			var totalEnabled = d3.sum(data.map(function(d) {
  				return (d.enabled) ? 1 : 0;
  			}));

  			if (rect.attr('class') === 'disabled') {
  				rect.attr('class', '');
  			} else {
  				if (totalEnabled < 2) return;
  				rect.attr('class', 'disabled');
  				enabled = false;
  	    }

  			pie.value(function(d) {
  				if (d.key === label) d.enabled = enabled;
  				return (d.enabled) ? d.value : 0;
  			});

  			path = path.data(pie(data));

  			path.transition()
          .duration(750)
  		    .attrTween('d', function(d) {
    			 	var interpolate = d3.interpolate(this._current, d);
    				this._current = interpolate(0);
    				return function(t) {
    					return arc(interpolate(t));
    				};
  		    });

  		});

  	legend.append('text')
  	.attr('x', legendRectSize + legendSpacing)
  	.attr('y', legendRectSize - legendSpacing)
  	.text(function(d) { return d; })

  });

}
