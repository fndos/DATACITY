# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField
from main.models import User

class Graph(models.Model):
    GRAPH_TYPE_CHOICES = (
      (None, 'Seleccione una opción'),
      (1, 'Tree Map'),
      (2, 'Bar Chart'),
      (3, 'Donut Chart'),
      (4, 'Bubble Chart'),
    )
    name = models.CharField(max_length=50)
    graph_type = models.PositiveSmallIntegerField(null=True, choices=GRAPH_TYPE_CHOICES)
    date_updated = models.DateTimeField(auto_now=True)
    graph_label = models.CharField(max_length=25)
    style = JSONField() # Almacenar aqui un JSON para definir el estilo del grafico
    data = JSONField() # Almacenar aqui un JSON donde estaran definidos los datos del grafico (ESTO HACE ESTATICO EL GRAFICO)
    clients = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pertenece_a')
    created_by = models.IntegerField()
