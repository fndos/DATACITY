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
	if (size == 4) { return "-152 0 712 712" }
	else if (size == 5) { return "-152 0 675 675" }
	else if (size == 6) { return "-152 0 675 675" }
	else { return "-152 0 675 675" }
}

function d3LineChartSample(container, source, date, size) {
  var svg = d3.select("svg"),
    margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom;
  var x = d3.scaleBand().rangeRound([0, width]).padding(0.1),
      y = d3.scaleLinear().rangeRound([height, 0]);
  var g = svg.append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  d3.json("http://127.0.0.1:8000/api/" + source + "/" + date + "/" , function(error, root) {

    var line = d3.line()
      .x(function(d) { return x(d.key); })
      .y(function(d) { return y(d.value); })

    x.domain(data.map(function(d) { return d.letter; }));

    y.domain([0, d3.max(data, function(d) { return d.frequency; })]);
    g.append("g")
        .attr("class", "axis axis--x")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    g.append("g")
        .attr("class", "axis axis--y")
        .call(d3.axisLeft(y).ticks(10, "%"))
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", "0.71em")
        .attr("text-anchor", "end")
        .text("Frequency");

    g.append("path")
      .datum(data)
      .attr("class", "line")
      .attr("d", line);

    g.selectAll("circle")
      .data(data)
    .enter().append("circle")
      .attr("class", "circle")
      .attr("cx", function(d) { return x(d.letter); })
      .attr("cy", function(d) { return y(d.frequency); })
      .attr("r", 4);
  });

}
