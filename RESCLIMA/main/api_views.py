# -*- coding: utf-8 -*-
from rest_framework import viewsets
from timeSeries import models
from . import serializers

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

import json

class VariableViewset(viewsets.ModelViewSet):
	queryset = models.Variable.objects.all()
	serializer_class = serializers.VariableSerializer

class StationTypeViewset(viewsets.ModelViewSet):
	queryset = models.StationType.objects.all()
	serializer_class = serializers.StationTypeSerializer

class StationViewset(viewsets.ModelViewSet):
	queryset = models.Station.objects.all()
	serializer_class = serializers.StationSerializer

# Esta clase por el momento no se esta utilizando en RESCLIMA
class ProviderViewSet(viewsets.ModelViewSet):
	queryset = models.Provider.objects.all()
	serializer_class = serializers.ProviderSerializer

class MeasurementViewSet(viewsets.ModelViewSet):
	queryset = models.Measurement.objects.all()
	serializer_class = serializers.MeasurementSerializer

class BubbleChartViewSet(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, format=None):
		station = models.StationType.objects.extra(select={'key': 'brand', 'value':'id'}).values('key', 'value')
		content = {
			"name": "Root",
			"children": [
				{
					"name": "Station",
					"children": station
				}
			]
		}

		return Response(content)

class BubbleChartMixedViewSet(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, format=None):
		variable = models.Variable.objects.extra(select={'key':'name', 'value':'id'}).values('key', 'value')
		station = models.StationType.objects.extra(select={'key': 'brand', 'value':'id'}).values('key', 'value')
		content = {
			"name": "Root",
			"children": [
				{
					"name": "Station",
					"children": station
				},
				{
					"name": "Variable",
					"children": variable
				}
			]
		}

		return Response(content)

class BubbleChartSampleViewSet(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, format=None):
		content = { "name": "flare", "children": [ { "name": "analytics", "children": [ { "name": "cluster", "children": [ {"name": "AgglomerativeCluster", "size": 3938}, {"name": "CommunityStructure", "size": 3812}, {"name": "HierarchicalCluster", "size": 6714}, {"name": "MergeEdge", "size": 743} ] }, { "name": "graph", "children": [ {"name": "BetweennessCentrality", "size": 3534}, {"name": "LinkDistance", "size": 5731}, {"name": "MaxFlowMinCut", "size": 7840}, {"name": "ShortestPaths", "size": 5914}, {"name": "SpanningTree", "size": 3416} ] }, { "name": "optimization", "children": [ {"name": "AspectRatioBanker", "size": 7074} ] } ] }, { "name": "animate", "children": [ {"name": "Easing", "size": 17010}, {"name": "FunctionSequence", "size": 5842}, { "name": "interpolate", "children": [ {"name": "ArrayInterpolator", "size": 1983}, {"name": "ColorInterpolator", "size": 2047}, {"name": "DateInterpolator", "size": 1375}, {"name": "Interpolator", "size": 8746}, {"name": "MatrixInterpolator", "size": 2202}, {"name": "NumberInterpolator", "size": 1382}, {"name": "ObjectInterpolator", "size": 1629}, {"name": "PointInterpolator", "size": 1675}, {"name": "RectangleInterpolator", "size": 2042} ] }, {"name": "ISchedulable", "size": 1041}, {"name": "Parallel", "size": 5176}, {"name": "Pause", "size": 449}, {"name": "Scheduler", "size": 5593}, {"name": "Sequence", "size": 5534}, {"name": "Transition", "size": 9201}, {"name": "Transitioner", "size": 19975}, {"name": "TransitionEvent", "size": 1116}, {"name": "Tween", "size": 6006} ] }, { "name": "data", "children": [ { "name": "converters", "children": [ {"name": "Converters", "size": 721}, {"name": "DelimitedTextConverter", "size": 4294}, {"name": "GraphMLConverter", "size": 9800}, {"name": "IDataConverter", "size": 1314}, {"name": "JSONConverter", "size": 2220} ] }, {"name": "DataField", "size": 1759}, {"name": "DataSchema", "size": 2165}, {"name": "DataSet", "size": 586}, {"name": "DataSource", "size": 3331}, {"name": "DataTable", "size": 772}, {"name": "DataUtil", "size": 3322} ] }, { "name": "display", "children": [ {"name": "DirtySprite", "size": 8833}, {"name": "LineSprite", "size": 1732}, {"name": "RectSprite", "size": 3623}, {"name": "TextSprite", "size": 10066} ] }, { "name": "flex", "children": [ {"name": "FlareVis", "size": 4116} ] }, { "name": "physics", "children": [ {"name": "DragForce", "size": 1082}, {"name": "GravityForce", "size": 1336}, {"name": "IForce", "size": 319}, {"name": "NBodyForce", "size": 10498}, {"name": "Particle", "size": 2822}, {"name": "Simulation", "size": 9983}, {"name": "Spring", "size": 2213}, {"name": "SpringForce", "size": 1681} ] }, { "name": "query", "children": [ {"name": "AggregateExpression", "size": 1616}, {"name": "And", "size": 1027}, {"name": "Arithmetic", "size": 3891}, {"name": "Average", "size": 891}, {"name": "BinaryExpression", "size": 2893}, {"name": "Comparison", "size": 5103}, {"name": "CompositeExpression", "size": 3677}, {"name": "Count", "size": 781}, {"name": "DateUtil", "size": 4141}, {"name": "Distinct", "size": 933}, {"name": "Expression", "size": 5130}, {"name": "ExpressionIterator", "size": 3617}, {"name": "Fn", "size": 3240}, {"name": "If", "size": 2732}, {"name": "IsA", "size": 2039}, {"name": "Literal", "size": 1214}, {"name": "Match", "size": 3748}, {"name": "Maximum", "size": 843}, { "name": "methods", "children": [ {"name": "add", "size": 593}, {"name": "and", "size": 330}, {"name": "average", "size": 287}, {"name": "count", "size": 277}, {"name": "distinct", "size": 292}, {"name": "div", "size": 595}, {"name": "eq", "size": 594}, {"name": "fn", "size": 460}, {"name": "gt", "size": 603}, {"name": "gte", "size": 625}, {"name": "iff", "size": 748}, {"name": "isa", "size": 461}, {"name": "lt", "size": 597}, {"name": "lte", "size": 619}, {"name": "max", "size": 283}, {"name": "min", "size": 283}, {"name": "mod", "size": 591}, {"name": "mul", "size": 603}, {"name": "neq", "size": 599}, {"name": "not", "size": 386}, {"name": "or", "size": 323}, {"name": "orderby", "size": 307}, {"name": "range", "size": 772}, {"name": "select", "size": 296}, {"name": "stddev", "size": 363}, {"name": "sub", "size": 600}, {"name": "sum", "size": 280}, {"name": "update", "size": 307}, {"name": "variance", "size": 335}, {"name": "where", "size": 299}, {"name": "xor", "size": 354}, {"name": "_", "size": 264} ] }, {"name": "Minimum", "size": 843}, {"name": "Not", "size": 1554}, {"name": "Or", "size": 970}, {"name": "Query", "size": 13896}, {"name": "Range", "size": 1594}, {"name": "StringUtil", "size": 4130}, {"name": "Sum", "size": 791}, {"name": "Variable", "size": 1124}, {"name": "Variance", "size": 1876}, {"name": "Xor", "size": 1101} ] }, { "name": "scale", "children": [ {"name": "IScaleMap", "size": 2105}, {"name": "LinearScale", "size": 1316}, {"name": "LogScale", "size": 3151}, {"name": "OrdinalScale", "size": 3770}, {"name": "QuantileScale", "size": 2435}, {"name": "QuantitativeScale", "size": 4839}, {"name": "RootScale", "size": 1756}, {"name": "Scale", "size": 4268}, {"name": "ScaleType", "size": 1821}, {"name": "TimeScale", "size": 5833} ] }, { "name": "util", "children": [ {"name": "Arrays", "size": 8258}, {"name": "Colors", "size": 10001}, {"name": "Dates", "size": 8217}, {"name": "Displays", "size": 12555}, {"name": "Filter", "size": 2324}, {"name": "Geometry", "size": 10993}, { "name": "heap", "children": [ {"name": "FibonacciHeap", "size": 9354}, {"name": "HeapNode", "size": 1233} ] }, {"name": "IEvaluable", "size": 335}, {"name": "IPredicate", "size": 383}, {"name": "IValueProxy", "size": 874}, { "name": "math", "children": [ {"name": "DenseMatrix", "size": 3165}, {"name": "IMatrix", "size": 2815}, {"name": "SparseMatrix", "size": 3366} ] }, {"name": "Maths", "size": 17705}, {"name": "Orientation", "size": 1486}, { "name": "palette", "children": [ {"name": "ColorPalette", "size": 6367}, {"name": "Palette", "size": 1229}, {"name": "ShapePalette", "size": 2059}, {"name": "SizePalette", "size": 2291} ] }, {"name": "Property", "size": 5559}, {"name": "Shapes", "size": 19118}, {"name": "Sort", "size": 6887}, {"name": "Stats", "size": 6557}, {"name": "Strings", "size": 22026} ] }, { "name": "vis", "children": [ { "name": "axis", "children": [ {"name": "Axes", "size": 1302}, {"name": "Axis", "size": 24593}, {"name": "AxisGridLine", "size": 652}, {"name": "AxisLabel", "size": 636}, {"name": "CartesianAxes", "size": 6703} ] }, { "name": "controls", "children": [ {"name": "AnchorControl", "size": 2138}, {"name": "ClickControl", "size": 3824}, {"name": "Control", "size": 1353}, {"name": "ControlList", "size": 4665}, {"name": "DragControl", "size": 2649}, {"name": "ExpandControl", "size": 2832}, {"name": "HoverControl", "size": 4896}, {"name": "IControl", "size": 763}, {"name": "PanZoomControl", "size": 5222}, {"name": "SelectionControl", "size": 7862}, {"name": "TooltipControl", "size": 8435} ] }, { "name": "data", "children": [ {"name": "Data", "size": 20544}, {"name": "DataList", "size": 19788}, {"name": "DataSprite", "size": 10349}, {"name": "EdgeSprite", "size": 3301}, {"name": "NodeSprite", "size": 19382}, { "name": "render", "children": [ {"name": "ArrowType", "size": 698}, {"name": "EdgeRenderer", "size": 5569}, {"name": "IRenderer", "size": 353}, {"name": "ShapeRenderer", "size": 2247} ] }, {"name": "ScaleBinding", "size": 11275}, {"name": "Tree", "size": 7147}, {"name": "TreeBuilder", "size": 9930} ] }, { "name": "events", "children": [ {"name": "DataEvent", "size": 2313}, {"name": "SelectionEvent", "size": 1880}, {"name": "TooltipEvent", "size": 1701}, {"name": "VisualizationEvent", "size": 1117} ] }, { "name": "legend", "children": [ {"name": "Legend", "size": 20859}, {"name": "LegendItem", "size": 4614}, {"name": "LegendRange", "size": 10530} ] }, { "name": "operator", "children": [ { "name": "distortion", "children": [ {"name": "BifocalDistortion", "size": 4461}, {"name": "Distortion", "size": 6314}, {"name": "FisheyeDistortion", "size": 3444} ] }, { "name": "encoder", "children": [ {"name": "ColorEncoder", "size": 3179}, {"name": "Encoder", "size": 4060}, {"name": "PropertyEncoder", "size": 4138}, {"name": "ShapeEncoder", "size": 1690}, {"name": "SizeEncoder", "size": 1830} ] }, { "name": "filter", "children": [ {"name": "FisheyeTreeFilter", "size": 5219}, {"name": "GraphDistanceFilter", "size": 3165}, {"name": "VisibilityFilter", "size": 3509} ] }, {"name": "IOperator", "size": 1286}, { "name": "label", "children": [ {"name": "Labeler", "size": 9956}, {"name": "RadialLabeler", "size": 3899}, {"name": "StackedAreaLabeler", "size": 3202} ] }, { "name": "layout", "children": [ {"name": "AxisLayout", "size": 6725}, {"name": "BundledEdgeRouter", "size": 3727}, {"name": "CircleLayout", "size": 9317}, {"name": "CirclePackingLayout", "size": 12003}, {"name": "DendrogramLayout", "size": 4853}, {"name": "ForceDirectedLayout", "size": 8411}, {"name": "IcicleTreeLayout", "size": 4864}, {"name": "IndentedTreeLayout", "size": 3174}, {"name": "Layout", "size": 7881}, {"name": "NodeLinkTreeLayout", "size": 12870}, {"name": "PieLayout", "size": 2728}, {"name": "RadialTreeLayout", "size": 12348}, {"name": "RandomLayout", "size": 870}, {"name": "StackedAreaLayout", "size": 9121}, {"name": "TreeMapLayout", "size": 9191} ] }, {"name": "Operator", "size": 2490}, {"name": "OperatorList", "size": 5248}, {"name": "OperatorSequence", "size": 4190}, {"name": "OperatorSwitch", "size": 2581}, {"name": "SortOperator", "size": 2023} ] }, {"name": "Visualization", "size": 16540} ] } ] }

		return Response(content)

class SunburstPartitionChartViewSet(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, format=None):
		variable = models.Variable.objects.extra(select={'key':'name', 'value':'id'}).values('key', 'value')
		station = models.StationType.objects.extra(select={'key': 'brand', 'value':'id'}).values('key', 'value')
		content = {
			"name": "Root",
			"children": [
				{
					"name": "Station",
					"children": station
				},
				{
					"name": "Variable",
					"children": variable
				},
				{
					"name": "Station",
					"children": station
				},
				{
					"name": "Variable",
					"children": variable
				},
				{
					"name": "Station",
					"children": station
				},
				{
					"name": "Variable",
					"children": variable
				}
			]
		}

		return Response(content)

class TreeMapViewSet(viewsets.ViewSet):
	renderer_classes = (JSONRenderer, )

	def list(self, request, format=None):
		content = [
		  {
		    "region": "Asia",
		    "subregion": "Southern Asia",
		    "value": 25500100,
		    "key": "Afghanistan"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Northern Europe",
		    "value": 28502,
		    "key": "Åland Islands"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Southern Europe",
		    "value": 2821977,
		    "key": "Albania"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Northern Africa",
		    "value": 37900000,
		    "key": "Algeria"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Southern Europe",
		    "value": 76246,
		    "key": "Andorra"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Middle Africa",
		    "value": 20609294,
		    "key": "Angola"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Caribbean",
		    "value": 13452,
		    "key": "Anguilla"
		  },
		  {
		    "region": "",
		    "subregion": "",
		    "value": -1,
		    "key": "Antarctica"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Caribbean",
		    "value": 86295,
		    "key": "Antigua and Barbuda"
		  },
		  {
		    "region": "Americas",
		    "subregion": "South America",
		    "value": 40117096,
		    "key": "Argentina"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Western Asia",
		    "value": 3024100,
		    "key": "Armenia"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Caribbean",
		    "value": 101484,
		    "key": "Aruba"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Western Europe",
		    "value": 8501502,
		    "key": "Austria"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Western Asia",
		    "value": 9235100,
		    "key": "Azerbaijan"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Caribbean",
		    "value": -1,
		    "key": "Bahamas"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Western Asia",
		    "value": 1234571,
		    "key": "Bahrain"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Southern Asia",
		    "value": 152518015,
		    "key": "Bangladesh"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Caribbean",
		    "value": 274200,
		    "key": "Barbados"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Eastern Europe",
		    "value": 9465500,
		    "key": "Belarus"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Western Europe",
		    "value": 11175653,
		    "key": "Belgium"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Central America",
		    "value": 312971,
		    "key": "Belize"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Western Africa",
		    "value": 10323000,
		    "key": "Benin"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Northern America",
		    "value": 64237,
		    "key": "Bermuda"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Southern Asia",
		    "value": 740990,
		    "key": "Bhutan"
		  },
		  {
		    "region": "Americas",
		    "subregion": "South America",
		    "value": 10027254,
		    "key": "Bolivia"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Caribbean",
		    "value": -1,
		    "key": "Bonaire"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Southern Europe",
		    "value": 3791622,
		    "key": "Bosnia and Herzegovina"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Southern Africa",
		    "value": 2024904,
		    "key": "Botswana"
		  },
		  {
		    "region": "",
		    "subregion": "",
		    "value": -1,
		    "key": "Bouvet Island"
		  },
		  {
		    "region": "Americas",
		    "subregion": "South America",
		    "value": 201032714,
		    "key": "Brazil"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Eastern Africa",
		    "value": -1,
		    "key": "British Indian Ocean Territory"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Caribbean",
		    "value": 29537,
		    "key": "British Virgin Islands"
		  },
		  {
		    "region": "Asia",
		    "subregion": "South-Eastern Asia",
		    "value": 393162,
		    "key": "Brunei"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Eastern Europe",
		    "value": 7282041,
		    "key": "Bulgaria"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Western Africa",
		    "value": 17322796,
		    "key": "Burkina Faso"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Eastern Africa",
		    "value": 10163000,
		    "key": "Burundi"
		  },
		  {
		    "region": "Asia",
		    "subregion": "South-Eastern Asia",
		    "value": 15135000,
		    "key": "Cambodia"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Middle Africa",
		    "value": 20386799,
		    "key": "Cameroon"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Northern America",
		    "value": 35158304,
		    "key": "Canada"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Western Africa",
		    "value": 491875,
		    "key": "Cape Verde"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Caribbean",
		    "value": 55456,
		    "key": "Cayman Islands"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Middle Africa",
		    "value": 4616000,
		    "key": "Central African Republic"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Middle Africa",
		    "value": 12825000,
		    "key": "Chad"
		  },
		  {
		    "region": "Americas",
		    "subregion": "South America",
		    "value": 16634603,
		    "key": "Chile"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Eastern Asia",
		    "value": 1361170000,
		    "key": "China"
		  },
		  {
		    "region": "Americas",
		    "subregion": "South America",
		    "value": 47330000,
		    "key": "Colombia"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Eastern Africa",
		    "value": 724300,
		    "key": "Comoros"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Middle Africa",
		    "value": 4448000,
		    "key": "Republic of the Congo"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Middle Africa",
		    "value": 67514000,
		    "key": "Democratic Republic of the Congo"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Central America",
		    "value": 4667096,
		    "key": "Costa Rica"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Western Africa",
		    "value": -1,
		    "key": "Côte d'Ivoire"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Southern Europe",
		    "value": 4290612,
		    "key": "Croatia"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Caribbean",
		    "value": 11167325,
		    "key": "Cuba"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Caribbean",
		    "value": 150563,
		    "key": "Curaçao"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Western Asia",
		    "value": 865878,
		    "key": "Cyprus"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Eastern Europe",
		    "value": 10512900,
		    "key": "Czech Republic"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Northern Europe",
		    "value": 5623501,
		    "key": "Denmark"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Eastern Africa",
		    "value": 864618,
		    "key": "Djibouti"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Caribbean",
		    "value": 71293,
		    "key": "Dominica"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Caribbean",
		    "value": 9445281,
		    "key": "Dominican Republic"
		  },
		  {
		    "region": "Americas",
		    "subregion": "South America",
		    "value": 15617900,
		    "key": "Ecuador"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Northern Africa",
		    "value": 83661000,
		    "key": "Egypt"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Central America",
		    "value": 6340000,
		    "key": "El Salvador"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Middle Africa",
		    "value": 1622000,
		    "key": "Equatorial Guinea"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Eastern Africa",
		    "value": 6333000,
		    "key": "Eritrea"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Northern Europe",
		    "value": 1286540,
		    "key": "Estonia"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Eastern Africa",
		    "value": 86613986,
		    "key": "Ethiopia"
		  },
		  {
		    "region": "Americas",
		    "subregion": "South America",
		    "value": 2563,
		    "key": "Falkland Islands"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Northern Europe",
		    "value": 48509,
		    "key": "Faroe Islands"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Northern Europe",
		    "value": 5445883,
		    "key": "Finland"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Western Europe",
		    "value": 65806000,
		    "key": "France"
		  },
		  {
		    "region": "Americas",
		    "subregion": "South America",
		    "value": 229040,
		    "key": "French Guiana"
		  },
		  {
		    "region": "",
		    "subregion": "",
		    "value": -1,
		    "key": "French Southern and Antarctic Lands"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Middle Africa",
		    "value": 1672000,
		    "key": "Gabon"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Western Africa",
		    "value": -1,
		    "key": "Gambia"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Western Asia",
		    "value": -1,
		    "key": "Georgia"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Western Europe",
		    "value": 80523700,
		    "key": "Germany"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Western Africa",
		    "value": 24658823,
		    "key": "Ghana"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Southern Europe",
		    "value": 29752,
		    "key": "Gibraltar"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Southern Europe",
		    "value": 10815197,
		    "key": "Greece"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Northern America",
		    "value": 56370,
		    "key": "Greenland"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Caribbean",
		    "value": 103328,
		    "key": "Grenada"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Caribbean",
		    "value": 403355,
		    "key": "Guadeloupe"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Central America",
		    "value": 15438384,
		    "key": "Guatemala"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Northern Europe",
		    "value": 62431,
		    "key": "Guernsey"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Western Africa",
		    "value": 10824200,
		    "key": "Guinea"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Western Africa",
		    "value": 1704000,
		    "key": "Guinea-Bissau"
		  },
		  {
		    "region": "Americas",
		    "subregion": "South America",
		    "value": 784894,
		    "key": "Guyana"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Caribbean",
		    "value": 10413211,
		    "key": "Haiti"
		  },
		  {
		    "region": "",
		    "subregion": "",
		    "value": -1,
		    "key": "Heard Island and McDonald Islands"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Southern Europe",
		    "value": 800,
		    "key": "Vatican City"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Central America",
		    "value": 8555072,
		    "key": "Honduras"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Eastern Asia",
		    "value": 7184000,
		    "key": "Hong Kong"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Eastern Europe",
		    "value": 9906000,
		    "key": "Hungary"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Northern Europe",
		    "value": 325010,
		    "key": "Iceland"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Southern Asia",
		    "value": 1236670000,
		    "key": "India"
		  },
		  {
		    "region": "Asia",
		    "subregion": "South-Eastern Asia",
		    "value": 237641326,
		    "key": "Indonesia"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Southern Asia",
		    "value": 77068000,
		    "key": "Iran"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Western Asia",
		    "value": 34035000,
		    "key": "Iraq"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Northern Europe",
		    "value": -1,
		    "key": "Ireland"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Northern Europe",
		    "value": 84497,
		    "key": "Isle of Man"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Western Asia",
		    "value": 8092700,
		    "key": "Israel"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Southern Europe",
		    "value": 59829079,
		    "key": "Italy"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Caribbean",
		    "value": 2711476,
		    "key": "Jamaica"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Eastern Asia",
		    "value": 127290000,
		    "key": "Japan"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Northern Europe",
		    "value": 97857,
		    "key": "Jersey"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Western Asia",
		    "value": 6512600,
		    "key": "Jordan"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Central Asia",
		    "value": 17099000,
		    "key": "Kazakhstan"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Eastern Africa",
		    "value": 44354000,
		    "key": "Kenya"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Western Asia",
		    "value": 3582054,
		    "key": "Kuwait"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Central Asia",
		    "value": 5551900,
		    "key": "Kyrgyzstan"
		  },
		  {
		    "region": "Asia",
		    "subregion": "South-Eastern Asia",
		    "value": 6580800,
		    "key": "Laos"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Northern Europe",
		    "value": 2014000,
		    "key": "Latvia"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Western Asia",
		    "value": 4822000,
		    "key": "Lebanon"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Southern Africa",
		    "value": 2074000,
		    "key": "Lesotho"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Western Africa",
		    "value": 4294000,
		    "key": "Liberia"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Northern Africa",
		    "value": 6202000,
		    "key": "Libya"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Western Europe",
		    "value": 36842,
		    "key": "Liechtenstein"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Northern Europe",
		    "value": 2950684,
		    "key": "Lithuania"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Western Europe",
		    "value": 537000,
		    "key": "Luxembourg"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Eastern Asia",
		    "value": -1,
		    "key": "Macau"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Southern Europe",
		    "value": -1,
		    "key": "Macedonia"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Eastern Africa",
		    "value": 20696070,
		    "key": "Madagascar"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Eastern Africa",
		    "value": 16363000,
		    "key": "Malawi"
		  },
		  {
		    "region": "Asia",
		    "subregion": "South-Eastern Asia",
		    "value": 29793600,
		    "key": "Malaysia"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Southern Asia",
		    "value": 317280,
		    "key": "Maldives"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Western Africa",
		    "value": 15302000,
		    "key": "Mali"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Southern Europe",
		    "value": 416055,
		    "key": "Malta"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Caribbean",
		    "value": 394173,
		    "key": "Martinique"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Western Africa",
		    "value": 3461041,
		    "key": "Mauritania"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Eastern Africa",
		    "value": 1257900,
		    "key": "Mauritius"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Eastern Africa",
		    "value": 212600,
		    "key": "Mayotte"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Central America",
		    "value": 118395054,
		    "key": "Mexico"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Eastern Europe",
		    "value": 3559500,
		    "key": "Moldova"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Western Europe",
		    "value": 36136,
		    "key": "Monaco"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Eastern Asia",
		    "value": 2754685,
		    "key": "Mongolia"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Southern Europe",
		    "value": 620029,
		    "key": "Montenegro"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Caribbean",
		    "value": 4922,
		    "key": "Montserrat"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Northern Africa",
		    "value": 33087700,
		    "key": "Morocco"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Eastern Africa",
		    "value": 23700715,
		    "key": "Mozambique"
		  },
		  {
		    "region": "Asia",
		    "subregion": "South-Eastern Asia",
		    "value": -1,
		    "key": "Myanmar"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Southern Africa",
		    "value": 2113077,
		    "key": "Namibia"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Southern Asia",
		    "value": 26494504,
		    "key": "Nepal"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Western Europe",
		    "value": 16807300,
		    "key": "Netherlands"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Central America",
		    "value": 6071045,
		    "key": "Nicaragua"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Western Africa",
		    "value": 17129076,
		    "key": "Niger"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Western Africa",
		    "value": 173615000,
		    "key": "Nigeria"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Eastern Asia",
		    "value": 24895000,
		    "key": "North Korea"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Northern Europe",
		    "value": 5077798,
		    "key": "Norway"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Western Asia",
		    "value": 3929000,
		    "key": "Oman"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Southern Asia",
		    "value": 184845000,
		    "key": "Pakistan"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Western Asia",
		    "value": -1,
		    "key": "Palestine"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Central America",
		    "value": 3405813,
		    "key": "Panama"
		  },
		  {
		    "region": "Americas",
		    "subregion": "South America",
		    "value": 6783374,
		    "key": "Paraguay"
		  },
		  {
		    "region": "Americas",
		    "subregion": "South America",
		    "value": 30475144,
		    "key": "Peru"
		  },
		  {
		    "region": "Asia",
		    "subregion": "South-Eastern Asia",
		    "value": 98678000,
		    "key": "Philippines"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Eastern Europe",
		    "value": 38533299,
		    "key": "Poland"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Southern Europe",
		    "value": 10562178,
		    "key": "Portugal"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Caribbean",
		    "value": 3667084,
		    "key": "Puerto Rico"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Western Asia",
		    "value": 2024707,
		    "key": "Qatar"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Eastern Europe",
		    "value": 1733842,
		    "key": "Republic of Kosovo"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Eastern Africa",
		    "value": 821136,
		    "key": "Réunion"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Eastern Europe",
		    "value": 20121641,
		    "key": "Romania"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Eastern Europe",
		    "value": 143500000,
		    "key": "Russia"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Eastern Africa",
		    "value": 10537222,
		    "key": "Rwanda"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Caribbean",
		    "value": 8938,
		    "key": "Saint Barthélemy"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Western Africa",
		    "value": -1,
		    "key": "Saint Helena"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Caribbean",
		    "value": 54000,
		    "key": "Saint Kitts and Nevis"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Caribbean",
		    "value": 166526,
		    "key": "Saint Lucia"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Caribbean",
		    "value": -1,
		    "key": "Saint Martin"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Northern America",
		    "value": 6081,
		    "key": "Saint Pierre and Miquelon"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Caribbean",
		    "value": 109000,
		    "key": "Saint Vincent and the Grenadines"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Southern Europe",
		    "value": 32509,
		    "key": "San Marino"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Middle Africa",
		    "value": 187356,
		    "key": "São Tomé and Príncipe"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Western Asia",
		    "value": 29994272,
		    "key": "Saudi Arabia"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Western Africa",
		    "value": 13567338,
		    "key": "Senegal"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Southern Europe",
		    "value": 7181505,
		    "key": "Serbia"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Eastern Africa",
		    "value": 90945,
		    "key": "Seychelles"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Western Africa",
		    "value": 6190280,
		    "key": "Sierra Leone"
		  },
		  {
		    "region": "Asia",
		    "subregion": "South-Eastern Asia",
		    "value": 5399200,
		    "key": "Singapore"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Caribbean",
		    "value": 37429,
		    "key": "Sint Maarten"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Eastern Europe",
		    "value": 5412008,
		    "key": "Slovakia"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Southern Europe",
		    "value": 2061405,
		    "key": "Slovenia"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Eastern Africa",
		    "value": 10496000,
		    "key": "Somalia"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Southern Africa",
		    "value": 52981991,
		    "key": "South Africa"
		  },
		  {
		    "region": "Americas",
		    "subregion": "South America",
		    "value": -1,
		    "key": "South Georgia"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Eastern Asia",
		    "value": 50219669,
		    "key": "South Korea"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Middle Africa",
		    "value": 11296000,
		    "key": "South Sudan"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Southern Europe",
		    "value": 46704314,
		    "key": "Spain"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Southern Asia",
		    "value": 20277597,
		    "key": "Sri Lanka"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Northern Africa",
		    "value": 37964000,
		    "key": "Sudan"
		  },
		  {
		    "region": "Americas",
		    "subregion": "South America",
		    "value": 534189,
		    "key": "Suriname"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Northern Europe",
		    "value": 2655,
		    "key": "Svalbard and Jan Mayen"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Southern Africa",
		    "value": 1250000,
		    "key": "Swaziland"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Northern Europe",
		    "value": 9625444,
		    "key": "Sweden"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Western Europe",
		    "value": 8085300,
		    "key": "Switzerland"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Western Asia",
		    "value": 21898000,
		    "key": "Syria"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Eastern Asia",
		    "value": 23361147,
		    "key": "Taiwan"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Central Asia",
		    "value": 8000000,
		    "key": "Tajikistan"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Eastern Africa",
		    "value": 44928923,
		    "key": "Tanzania"
		  },
		  {
		    "region": "Asia",
		    "subregion": "South-Eastern Asia",
		    "value": 65926261,
		    "key": "Thailand"
		  },
		  {
		    "region": "Asia",
		    "subregion": "South-Eastern Asia",
		    "value": -1,
		    "key": "Timor-Leste"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Western Africa",
		    "value": 6191155,
		    "key": "Togo"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Caribbean",
		    "value": 1328019,
		    "key": "Trinidad and Tobago"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Northern Africa",
		    "value": 10833431,
		    "key": "Tunisia"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Western Asia",
		    "value": 75627384,
		    "key": "Turkey"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Central Asia",
		    "value": 5240000,
		    "key": "Turkmenistan"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Caribbean",
		    "value": 31458,
		    "key": "Turks and Caicos Islands"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Eastern Africa",
		    "value": 35357000,
		    "key": "Uganda"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Eastern Europe",
		    "value": 45461627,
		    "key": "Ukraine"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Western Asia",
		    "value": 8264070,
		    "key": "United Arab Emirates"
		  },
		  {
		    "region": "Europe",
		    "subregion": "Northern Europe",
		    "value": 63705000,
		    "key": "United Kingdom"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Northern America",
		    "value": 317101000,
		    "key": "United States"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Northern America",
		    "value": -1,
		    "key": "United States Minor Outlying Islands"
		  },
		  {
		    "region": "Americas",
		    "subregion": "Caribbean",
		    "value": 106405,
		    "key": "United States Virgin Islands"
		  },
		  {
		    "region": "Americas",
		    "subregion": "South America",
		    "value": 3286314,
		    "key": "Uruguay"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Central Asia",
		    "value": 30183400,
		    "key": "Uzbekistan"
		  },
		  {
		    "region": "Americas",
		    "subregion": "South America",
		    "value": 28946101,
		    "key": "Venezuela"
		  },
		  {
		    "region": "Asia",
		    "subregion": "South-Eastern Asia",
		    "value": 90388000,
		    "key": "Vietnam"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Northern Africa",
		    "value": 567000,
		    "key": "Western Sahara"
		  },
		  {
		    "region": "Asia",
		    "subregion": "Western Asia",
		    "value": 24527000,
		    "key": "Yemen"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Eastern Africa",
		    "value": 13092666,
		    "key": "Zambia"
		  },
		  {
		    "region": "Africa",
		    "subregion": "Eastern Africa",
		    "value": 12973808,
		    "key": "Zimbabwe"
		  }
		]

		return Response(content)
