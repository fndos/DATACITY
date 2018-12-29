from rest_framework import viewsets
from timeSeries import models
from . import serializers

from rest_framework.decorators import api_view

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
