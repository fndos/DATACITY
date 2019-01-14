from rest_framework import routers
from django.conf.urls import include, url
from main import api_views

router = routers.DefaultRouter()
router.register(r'db_resclima_variables', api_views.VariableViewset)
router.register(r'db_resclima_station_types', api_views.StationTypeViewset)
router.register(r'db_resclima_stations', api_views.StationViewset)
router.register(r'db_resclima_providers', api_views.ProviderViewSet)
router.register(r'db_resclima_measurements', api_views.MeasurementViewSet)

router.register(r'db_resclima_average_measurement/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.APIAverageMeasurementViewSet, base_name='db_resclima_average_measurement')

router.register(r'd3_bubble_chart_sample', api_views.BubbleChartViewSet, base_name='d3_bubble_chart_sample')
router.register(r'd3_tree_map_sample', api_views.TreeMapViewSet, base_name='d3_tree_map_sample')

router.register(r'd3_bar_chart_L_ON/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.APILightONViewSet, base_name='d3_bar_chart_L_ON')
router.register(r'd3_bar_chart_L_OE/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.APILightOEViewSet, base_name='d3_bar_chart_L_OE')
router.register(r'd3_bar_chart_L_NE/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.APILightNEViewSet, base_name='d3_bar_chart_L_NE')
router.register(r'd3_bar_chart_W_ON/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.APIWeightONViewSet, base_name='d3_bar_chart_W_ON')
router.register(r'd3_bar_chart_W_OE/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.APIWeightOEViewSet, base_name='d3_bar_chart_W_OE')
router.register(r'd3_bar_chart_W_NE/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.APIWeightNEViewSet, base_name='d3_bar_chart_W_NE')

router.register(r'd3_pie_chart_composition_ON/(?P<date>[-\w]+)', api_views.APICompositionONViewSet, base_name='d3_pie_chart_composition_ON')
router.register(r'd3_pie_chart_composition_OE/(?P<date>[-\w]+)', api_views.APICompositionOEViewSet, base_name='d3_pie_chart_composition_OE')
router.register(r'd3_pie_chart_composition_NE/(?P<date>[-\w]+)', api_views.APICompositionNEViewSet, base_name='d3_pie_chart_composition_NE')
router.register(r'd3_pie_chart_composition/(?P<date>[-\w]+)', api_views.APICompositionViewSet, base_name='d3_pie_chart_composition')
