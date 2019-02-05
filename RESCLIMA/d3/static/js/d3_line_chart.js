// ******************************************************************
// ************************* Simple function ************************
// ******************************************************************

function toTitleCase(str) {
    return str.replace(/\w\S*/g, function(txt){
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
}

function getLineChartPluginSize(str) {
  return parseInt(str[str.length-1]);
}

function getLineChartViewBox(size) {
	if (size == 4) { return "6 0 1062 425" }
	else if (size == 5) { return "6 0 842 325" }
	else if (size == 6) { return "6 0 700 270" }
	else { return "4 0 586 270" } // OK
}

function setSource(sid, source, start_date, end_date) {
	if (!sid) { return "http://127.0.0.1:8000/api/" + source + "/" + start_date + "/" + end_date + "/"; }
	else { return "http://127.0.0.1:8000/api/" + source + "/" + sid; }
}

function setOrigin(sid, origin, start_date, end_date) {
	if (!sid) { return "http://127.0.0.1:8000/api/" + origin + "/" + start_date + "/" + end_date + "/"; }
	else { return "http://127.0.0.1:8000/api/" + origin + "/" + sid; }
}

function isEmpty(str) {
	if (!str) { return true; }
	else { return false }
}

function checkDate(start_date, end_date) {
   if (!isEmpty(start_date) && !isEmpty(end_date)) { return true; }
  else { return false; }
}

function setLegend(str) {
  if (str.includes("W")) {
    return "Pesados"
  } else if (str.includes("L")) {
    return "Livianos"
  } else {
    return "Undefined"
  }
}

function d3LineChartSample(container, start_date, end_date, source, origin, domainLabel, rangeLabel, size, sid) {
  if (!checkDate(start_date, end_date)) {
    // Una de las fechas ingresadas no es valida
    start_date = null;
    end_date = null;
  }

  SOURCE_URL = setSource(sid, source, start_date, end_date);
  ORIGIN_URL = setOrigin(sid, origin, start_date, end_date);

  // Set the dimensions of the canvas / graph
  var	margin = {top: 30, right: 20, bottom: 30, left: 50},
  	  width = 586 - margin.left - margin.right, // 600
  	  height = 270 - margin.top - margin.bottom; // 270

  // Set the ranges
  var x = d3.scale.linear().range([0 , width]),
  y = d3.scale.linear().range([height, 0]);

  // Define the axes
  var	xAxis = d3.svg.axis().scale(x);

  var	yAxis = d3.svg.axis().scale(y)
  	.orient("left")
    .tickFormat(function (d) {
        var prefix = d3.formatPrefix(d);
        return prefix.scale(d) + prefix.symbol;
    });

  // Define the line
  var	line = d3.svg.line()
    .x(function(d) { return x(d.key); })
    .y(function(d) { return y(d.value); });
    // .interpolate("basis");

  // Adds the svg canvas
  var	svg = d3.select(container)
    .append("svg")
    .attr("viewBox", getLineChartViewBox(getLineChartPluginSize(size)))
    .attr("perserveAspectRatio", "xMinYMid")
    .attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  // Add tooltip
  var tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function(d) {
      return "<span>" + domainLabel + ": </span><span style='color: white;'>" + d.key + "</span><br/>" +
             "<span>" + rangeLabel + ": </span><span style='color: white;'>" + d.value + "</span>"
    });

  // BUG: Llamar tooltip solo en 7x7
  if (getLineChartPluginSize(size) == 7) { svg.call(tip); }

  d3.queue()
    .defer(d3.json, SOURCE_URL)
    .defer(d3.json, ORIGIN_URL)
    .await(function(error, data, data2) {
    if (error) {
        console.error('Algo salió mal: ' + error);
    }
    else {
        // Escoger el maximo y
        data_max = d3.max(data, function(d) { return d.value });
        data2_max = d3.max(data2, function(d) { return d.value });
        // Scale the range of the data
      	x.domain(d3.extent(data, function(d) { return d.key }));
        y.domain([0, Math.max(data_max, data2_max)]);

      	// Add the line path.
      	svg.append("path")
      		.attr("class", "line")
      		.attr("d", line(data))
          .attr("data-legend",function(d) { return setLegend(source) });

        // circles
        svg.selectAll(".dot")
        	.data(data)
      	   //.defined(function(d) { return d.data_point == true; })
          .enter().append("circle")
          .attr("class", "dot")
          .style("stroke", "blue")
          .style("fill", "blue")
          .attr("r", 3)
          .attr("cx", function(d) { return x(d.key); })
          .attr("cy", function(d) { return y(d.value); })
      	  .on("mouseover", function(d) {tip.show(d);} )
          .on("mouseout", function(d) {tip.hide(d);} );

      	// Add the X Axis
      	svg.append("g")
      		.attr("class", "x axis")
      		.attr("transform", "translate(0," + height + ")")
      		.call(xAxis)
          .append("text").style("font-size", "14px")
          .attr("x", width / 2 + 13)
          .attr("y",  30)
          .attr("dx", ".75em")
          .style("text-anchor", "end")
          .text(domainLabel);

      	// Add the Y Axis
      	svg.append("g")
      		.attr("class", "y axis")
      		.call(yAxis)
          .append("text").style("font-size", "14px")
          .attr("y", -34)
          .attr("x", -(height)/ 2 + margin.top + 5)
          .attr("transform", "rotate(-90)")
          .style("text-anchor", "end")
          .text(rangeLabel);

      	// Add the line path.
      	svg.append("path")
      		.attr("class", "line")
          .style("stroke", "red")
      		.attr("d", line(data2))
          .attr("data-legend",function(d) { return setLegend(origin) });

        // circles
        svg.selectAll(".dot2")
        	.data(data2)
      	   //.defined(function(d) { return d.data_point == true; })
          .enter().append("circle")
          .attr("class", "dot2")
          .style("stroke", "red")
          .style("fill", "red")
          .attr("r", 3)
          .attr("cx", function(d) { return x(d.key); })
          .attr("cy", function(d) { return y(d.value); })
      	  .on("mouseover", function(d) {tip.show(d);} )
          .on("mouseout", function(d) {tip.hide(d);} );

        legend = svg.append("g")
          .attr("class","legend")
          .attr("transform","translate(474,-22)")
          .style("font-size","12px")
          .call(d3.legend)

    }
  });

}
