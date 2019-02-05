from rest_framework import routers
from django.conf.urls import include, url
from main import api_views

router = routers.DefaultRouter()

# Grafico de barras para los investigadores de ESPOL
router.register(r'db_resclima_average_measurement/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.Medicion, base_name='db_resclima_average_measurement') # OK

# Grafico de barras para los investigadores de logistica y transporte (livianos)
router.register(r'd3_bar_chart_L_EN/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.LEN, base_name='d3_bar_chart_L_EN') # OK
router.register(r'd3_bar_chart_L_EO/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.LEO, base_name='d3_bar_chart_L_EO')
router.register(r'd3_bar_chart_L_NO/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.LNO, base_name='d3_bar_chart_L_NO')
router.register(r'd3_bar_chart_L_ON/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.LON, base_name='d3_bar_chart_L_ON')
router.register(r'd3_bar_chart_L_OE/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.LOE, base_name='d3_bar_chart_L_OE')
router.register(r'd3_bar_chart_L_NE/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.LNE, base_name='d3_bar_chart_L_NE')

# Grafico de barras para los investigadores de logistica y transporte (pesados)
router.register(r'd3_bar_chart_W_EN/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.WEN, base_name='d3_bar_chart_W_EN') # OK
router.register(r'd3_bar_chart_W_EO/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.WEO, base_name='d3_bar_chart_W_EO')
router.register(r'd3_bar_chart_W_NO/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.WNO, base_name='d3_bar_chart_W_NO')
router.register(r'd3_bar_chart_W_ON/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.WON, base_name='d3_bar_chart_W_ON')
router.register(r'd3_bar_chart_W_OE/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.WOE, base_name='d3_bar_chart_W_OE')
router.register(r'd3_bar_chart_W_NE/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.WNE, base_name='d3_bar_chart_W_NE')

# Grafico de barras (composicion %) para los investigadores de logistica y transporte
router.register(r'd3_pie_chart_composition_EN/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.CEN, base_name='d3_pie_chart_composition_EN') # OK
router.register(r'd3_pie_chart_composition_EO/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.CEO, base_name='d3_pie_chart_composition_EO')
router.register(r'd3_pie_chart_composition_NO/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.CNO, base_name='d3_pie_chart_composition_NO')
router.register(r'd3_pie_chart_composition_ON/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.CON, base_name='d3_pie_chart_composition_ON')
router.register(r'd3_pie_chart_composition_OE/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.COE, base_name='d3_pie_chart_composition_OE')
router.register(r'd3_pie_chart_composition_NE/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.CNE, base_name='d3_pie_chart_composition_NE')

# Grafico circular para los investigadores de logsitica y transporte
router.register(r'd3_pie_chart_WE/(?P<sid>[-\w]+)', api_views.WE, base_name='d3_pie_chart_WE') # OK
router.register(r'd3_pie_chart_LE/(?P<sid>[-\w]+)', api_views.LE, base_name='d3_pie_chart_LE') # OK

# Grafico de lineas para los investigadores de logistica y transporte
router.register(r'd3_line_chart_WMS/(?P<sid>[-\w]+)', api_views.WMS, base_name='d3_line_chart_LMS') # OK
router.register(r'd3_line_chart_LMS/(?P<sid>[-\w]+)', api_views.LMS, base_name='d3_line_chart_LMS') # OK
router.register(r'd3_line_chart_WT/(?P<sid>[-\w]+)', api_views.WWT, base_name='d3_line_chart_WT') # OK
router.register(r'd3_line_chart_LT/(?P<sid>[-\w]+)', api_views.LWT, base_name='d3_line_chart_LT') # OK


# Series de tiempo para los investigadores de cambio climatico
router.register(r'd3_time_series_tmin/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.Minimo, base_name='d3_time_series_tmin') # OK
router.register(r'd3_time_series_tmax/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.Maximo, base_name='d3_time_series_tmax') # OK
router.register(r'd3_time_series_tmean/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.Promedio, base_name='d3_time_series_tmean') # OK
router.register(r'd3_time_series_rr/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.RR, base_name='d3_time_series_rr') # OK
router.register(r'd3_time_series_oni/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.ONI, base_name='d3_time_series_oni') # OK

# Grafico circular para los investigadores de cambio climatico
router.register(r'd3_pie_chart_censo/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.Censo, base_name='d3_pie_chart_censo') # OK
# Grafico de barras para los investigadores de cambio climatico
router.register(r'd3_bar_chart_censo/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.CensoBar, base_name='d3_bar_chart_censo') # No se mira bien
router.register(r'd3_bar_chart_population/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.Population, base_name='d3_bar_chart_population') # OK
# Grafico de barras agrupadas para los investigadores de cambio climatico
router.register(r'd3_grouped_bar_chart/(?P<start_date>[-\w]+)/(?P<end_date>[-\w]+)', api_views.Precipitation, base_name='d3_grouped_bar_chart') # OK
