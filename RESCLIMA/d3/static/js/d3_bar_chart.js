// ******************************************************************
// ************************* Simple function ************************
// ******************************************************************

function toTitleCase(str) {
    return str.replace(/\w\S*/g, function(txt){
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
}

function d3BarChartSample(bubbleContainer, selected_table, selected_domain, selected_range, selected_label, selected_color) {
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
  var svg = d3.select(bubbleContainer).append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  d3.json("http://127.0.0.1:8000/api/" + selected_table + "/", function(error, data) {
    // get data from table
    console.log(data)

    data.forEach(function(d) {
      d[selected_domain] = d[selected_domain];
      d[selected_range] = +d[selected_range];
    });

    // scale the range of the data
    x.domain(data.map(function(d) { return d[selected_domain]; }));
    y.domain([0, d3.max(data, function(d) { return d.id; })]);

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
        .text(toTitleCase(selected_label));

    // Add bar chart
    svg.selectAll("bar")
        .data(data)
        .enter()
        .append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return x(d[selected_domain]); })
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(d[selected_range]); })
        .attr("height", function(d) { return height - y(d[selected_range]); })
        .attr("fill", function(d) { return selected_color });

  });

}
