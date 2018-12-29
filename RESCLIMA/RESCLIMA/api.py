from rest_framework import routers
from main import api_views

router = routers.DefaultRouter()
router.register(r'variables', api_views.VariableViewset)
router.register(r'station_types', api_views.StationTypeViewset)
router.register(r'stations', api_views.StationViewset)
router.register(r'providers', api_views.ProviderViewSet)
router.register(r'measurements', api_views.MeasurementViewSet)
