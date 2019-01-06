from rest_framework import routers
from main import api_views

router = routers.DefaultRouter()
router.register(r'variables', api_views.VariableViewset)
router.register(r'station_types', api_views.StationTypeViewset)
router.register(r'stations', api_views.StationViewset)
router.register(r'providers', api_views.ProviderViewSet)
router.register(r'measurements', api_views.MeasurementViewSet)
router.register(r'bubble', api_views.BubbleChartViewSet, base_name='bubble')
router.register(r'mixed', api_views.BubbleChartMixedViewSet, base_name='mixed')
router.register(r'sample', api_views.BubbleChartSampleViewSet, base_name='sample')
router.register(r'sunburst', api_views.SunburstPartitionChartViewSet, base_name='sunburst')
router.register(r'treemap', api_views.TreeMapViewSet, base_name='treemap')
router.register(r'apitest', api_views.APITestViewSet, base_name='apitest')
