// ******************************************************************
// ************************* Simple function ************************
// ******************************************************************

function getSunburstPluginSize(str) {
  return parseInt(str[str.length-1]);
}

function getSunburstViewBox(size) {
	if (size == 4) { return "0 0 425 245" }
	else if (size == 5) { return "0 0 525 325" }
	else if (size == 6) { return "0 0 525 365" }
	else { return "0 0 625 425" }
}

function d3SunburstPartitionChartSample(container, iWidth, iHeight, source, size) {
  var width = iWidth,
    height = iHeight,
    radius = Math.min(width, height) / 2,
    color = d3.scale.category20c();

  var svg = d3.select(container).append("svg")
    .attr("viewBox", getSunburstViewBox(getSunburstPluginSize(size)))
    .attr("perserveAspectRatio", "xMinYMid")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height * .52 + ")");

  var partition = d3.layout.partition()
    .sort(null)
    .size([2 * Math.PI, radius * radius])
    .value(function(d) { return 1; });

  var arc = d3.svg.arc()
    .startAngle(function(d) { return d.x; })
    .endAngle(function(d) { return d.x + d.dx; })
    .innerRadius(function(d) { return Math.sqrt(d.y); })
    .outerRadius(function(d) { return Math.sqrt(d.y + d.dy); });

  d3.json("http://127.0.0.1:8000/api/" + source + "/", function(error, root) {
    //console.log(root)
    var path = svg.datum(root).selectAll("path")
      .data(partition.nodes)
      .enter().append("path")
      .attr("display", function(d) { return d.depth ? null : "none"; }) // hide inner ring
      .attr("d", arc)
      .style("stroke", "#fff")
      .style("fill", function(d) { return color((d.children ? d : d.parent).name); })
      .style("fill-rule", "evenodd")
      .each(stash);

    d3.selectAll("input").on("change", function change() {
      var value = this.value === "count"
        ? function() { return 1; }
        : function(d) { return d.size; };
        // revisar si se debe reemplazar size por value

      path.data(partition.value(value).nodes)
        .transition()
        .duration(1500)
        .attrTween("d", arcTween);
    });
  });

  // Stash the old values for transition.
  function stash(d) {
    d.x0 = d.x;
    d.dx0 = d.dx;
  }

  // Interpolate the arcs in data space.
  function arcTween(a) {
    var i = d3.interpolate({x: a.x0, dx: a.dx0}, a);
    return function(t) {
      var b = i(t);
      a.x0 = b.x;
      a.dx0 = b.dx;
      return arc(b);
    };
  }

  d3.select(self.frameElement).style("height", height + "px");
}
