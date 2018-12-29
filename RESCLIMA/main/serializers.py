from rest_framework import serializers
from timeSeries import models

class VariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Variable
        fields = ('id', 'name', 'unit', 'symbol', 'datatype')

class StationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StationType
        fields = ('id', 'brand', 'model', 'automatic', 'variables')

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Station
        fields = ('id', 'serialNum', 'location', 'active', 'stationType', 'frequency', 'token')

# Esta clase por el momento no se esta utilizando en RESCLIMA
class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Provider
        fields = ('id', 'name', 'info')

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Measurement
        fields = ('id_m', 'ts', 'idStation', 'idProvider', 'readings', 'id_s')
