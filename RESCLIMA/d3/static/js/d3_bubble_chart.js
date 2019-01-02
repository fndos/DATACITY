// ******************************************************************
// ************************* Simple function ************************
// ******************************************************************

function d3BubbleChartSample(bubbleContainer, diameter, selected_source, bubblePadding, bubbleNodeDy, bubbleNodeTextAnchor) {
	// define the color
	var format = d3.format(",d"),
		color = d3.scale.category20c();

	// define the layout
	var bubble = d3.layout.pack()
		.sort(null)
		.size([diameter, diameter])
		.padding(bubblePadding);

	// add the SVG element
	var svg = d3.select(bubbleContainer)
		.append("svg")
		.attr("width", diameter)
		.attr("height", diameter)
		.attr("class", "bubble");

	d3.json("http://127.0.0.1:8000/api/" + selected_source + "/", function(error, root) {
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
			.attr("dy", bubbleNodeDy)
			.style("text-anchor", bubbleNodeTextAnchor)
			.text(function(d) { return d.className.substring(0, d.r / 3); });
	});

	// returns a flattened hierarchy containing all leaf nodes under the root
	function classes(root) {
		var classes = [];

		function recurse(name, node) {
			if (node.children) node.children.forEach(function(child) { recurse(node.name, child); });
			else classes.push({packageName: name, className: node.key, value: node.value});
		}

		recurse(null, root);
		return {children: classes};
	}

	d3.select(self.frameElement).style("height", diameter + "px");
}
