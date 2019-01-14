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
	if (size == 4) { return "12 0 589 589" }
	else if (size == 5) { return "12 0 589 589" }
	else if (size == 6) { return "12 0 589 589" }
	else { return "12 0 589 589" }
}

function d3LineChartSample(container, start_date, end_date, source, origin, domainLabel, rangeLabel, size) {
  // Set the dimensions of the canvas / graph
  var	margin = {top: 30, right: 20, bottom: 30, left: 50},
  	  width = 600 - margin.left - margin.right,
  	  height = 270 - margin.top - margin.bottom;

  // Set the ranges
  var x = d3.scale.linear().range([0 , width]),
  y = d3.scale.linear().range([height, 0]);

  // Define the axes
  var	xAxis = d3.svg.axis().scale(x);

  var	yAxis = d3.svg.axis().scale(y)
  	.orient("left");

  // Define the line
  var	line = d3.svg.line()
    .x(function(d) { return x(d.key); })
    .y(function(d) { return y(d.value); }).interpolate("basis");

  // Adds the svg canvas
  var	svg = d3.select(container)
    .append("svg")
    .attr("viewBox", getLineChartViewBox(getLineChartPluginSize(size)))
    .attr("perserveAspectRatio", "xMinYMid")
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  d3.json("http://127.0.0.1:8000/api/" + source + "/" + start_date + "/" + end_date + "/" , function(error, data) {

    console.log(data);
    // Scale the range of the data
  	x.domain(d3.extent(data, function(d) { return d.key; }));
  	y.domain([0, d3.max(data, function(d) { return d.value; })]);

  	// Add the line path.
  	svg.append("path")
  		.attr("class", "line")
  		.attr("d", line(data));

  	// Add the X Axis
  	svg.append("g")
  		.attr("class", "x axis")
  		.attr("transform", "translate(0," + height + ")")
  		.call(xAxis)
      .append("text")
      .attr("x", width / 2)
      .attr("y",  31)
      .attr("dx", ".75em")
      .style("text-anchor", "end")
      .text(toTitleCase(domainLabel));

  	// Add the Y Axis
  	svg.append("g")
  		.attr("class", "y axis")
  		.call(yAxis)
      .append("text")
      .attr("y", -31)
      .attr("x", -(height)/ 2 + margin.top)
      .attr("transform", "rotate(-90)")
      .style("text-anchor", "end")
      .text(toTitleCase(rangeLabel));

  });

  d3.json("http://127.0.0.1:8000/api/" + origin + "/" + start_date + "/" + end_date + "/" , function(error, data) {
  	// Add the line path.
    console.log(data);
  	svg.append("path")
  		.attr("class", "line2")
  		.attr("d", line(data));

  });

}
