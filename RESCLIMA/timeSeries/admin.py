from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(StationType)
admin.site.register(Variable)
admin.site.register(Station)
admin.site.register(Provider)
admin.site.register(Measurement)
