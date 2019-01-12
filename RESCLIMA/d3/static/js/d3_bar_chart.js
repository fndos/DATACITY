// ******************************************************************
// ************************* Simple function ************************
// ******************************************************************

function toTitleCase(str) {
    return str.replace(/\w\S*/g, function(txt){
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
}

function d3BarChartSample(container, source, date, domainLabel, rangeLabel, color, hover) {
  // set the dimensions of the canvas
  var margin = {top: 20, right: 20, bottom: 70, left: 40},
      width = 600 - margin.left - margin.right,
      height = 300 - margin.top - margin.bottom;

  // set the ranges
  var x = d3.scale.ordinal().rangeRoundBands([0, width], .05);

  var y = d3.scale.linear().range([height, 0]);

  // define the axis
  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom")

  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")
      .ticks(10);

  // add the SVG element
  console.log(container)
  var svg = d3.select(container).append("svg")
      .attr("preserveAspectRatio", "xMinYMin meet")
      .attr("viewBox", "0 -25 600 600")
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function(d) {
      return "<div><span>" + toTitleCase(domainLabel) + ":</span> <span style='color:white'>" + d['key'] + "</span></div>" +
             "<div><span>" + toTitleCase(rangeLabel) + ":</span> <span style='color:white'>" + d['value'] + "</span></div>";
    })

  svg.call(tip);
  d3.json("http://127.0.0.1:8000/api/" + source + "/" + date + "/" , function(error, data) {
    //console.log(data)

    // get data from table
    data.forEach(function(d) {
      d['key'] = d['key'];
      d['value'] = +d['value'];
    });

    // scale the range of the data
    x.domain(data.map(function(d) { return d['key']; }));
    y.domain([0, d3.max(data, function(d) { return d['value']; })]);

    // add axis
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
        .selectAll("text")
        .style("text-anchor", "end")
        .attr("dx", "-.8em")
        .attr("dy", "-.55em")
        .attr("transform", "rotate(-90)" );

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 5)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text(toTitleCase(rangeLabel));

    // Add bar chart
    svg.selectAll("bar")
        .data(data)
        .enter()
        .append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return x(d['key']); })
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(d['value']); })
        .attr("height", function(d) { return height - y(d['value']); })
        .attr("fill", function(d) { return color })
        .on("mouseover", function(d) {
          d3.select(this).style("fill", hover);
          tip.show(d);
        })
        .on("mouseout", function(d) {
          d3.select(this).style("fill", color);
          tip.hide(d);
        })

  });

}
