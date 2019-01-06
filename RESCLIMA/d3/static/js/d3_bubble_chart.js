// ******************************************************************
// ************************* Simple function ************************
// ******************************************************************

function getBubbleChartPluginSize(str) {
  return parseInt(str[str.length-1]);
}

function getBubbleChartViewBox(size) {
	if (size == 4) { return "0 0 325 575" }
	else if (size == 5) { return "0 0 425 775" }
	else if (size == 6) { return "0 0 525 875" }
	else { return "0 0 625 975" }
}

function setCustomKey(str) {
	if (!str) { return "key"; }
	else { return str; }
}

function setCustomValue(str) {
	if (!str) { return "value"; }
	else { return str; }
}

function d3BubbleChartSample(container, diameter, source, padding, nodeDy, nodeTextAnchor, size, key, value) {
	// check key and value
	key = setCustomKey(key);
	value = setCustomValue(value);

	// define the color
	var format = d3.format(",d"),
		color = d3.scale.category20c();

	// define the layout
	var bubble = d3.layout.pack()
		.sort(null)
		.size([diameter, diameter])
		.padding(padding);

	// add the SVG element
	var svg = d3.select(container)
		.append("svg")
		.attr("viewBox", getBubbleChartViewBox(getBubbleChartPluginSize(size)))
	  .attr("perserveAspectRatio", "xMinYMid")
	  .attr("width", diameter)
	  .attr("height", diameter)
	  .attr("class", "bubble");

	d3.json("http://127.0.0.1:8000/api/" + source + "/", function(error, root) {
		// loading data from root
		var node = svg.selectAll(".node")
			.data(bubble.nodes(classes(root))
			.filter(function(d) { return !d.children; }))
			.enter()
			.append("g")
			.attr("class", "node")
			.attr("transform", function(d) {
					return "translate(" + d.x + "," + d.y + ")";
			});

		node.append("title")
			.text(function(d) { return d.className + ": " + format(d.value); });

		node.append("circle")
			.attr("r", function(d) { return d.r; })
			.style("fill", function(d) { return color(d.packageName); });

		node.append("text")
		  .attr("dy", nodeDy)
			.style("text-anchor", nodeTextAnchor)
      .text(function(d) { return d.className.substring(0, d.r / 3); })
      .style("font-size", function(d) { return Math.min(2 * d.r, (2 * d.r - 8) / this.getComputedTextLength() * 12) + "px"; });


	});

	// returns a flattened hierarchy containing all leaf nodes under the root
	function classes(root) {
		var classes = [];

		function recurse(name, node) {
			if (node.children) node.children.forEach(function(child) { recurse(node.name, child); });
			else classes.push({packageName: name, className: node[key], value: node[value]});
		}

		recurse(null, root);
		return {children: classes};
	}

	d3.select(self.frameElement).style("height", diameter + "px");
}
