from dash.base import BaseDashboardLayout, BaseDashboardPlaceholder
from dash.base import layout_registry

# __title__ = 'dash.contrib.layouts.bootstrap2.dash_layouts'
# __author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
# __copyright__ = '2013-2018 Artur Barseghyan'
# __license__ = 'GPL 2.0/LGPL 2.1'
# __all__ = ('ProductoLayout',)

# *******************************************************************
# ***********************Layout del producto ************************
# *******************************************************************


class ProductoMainPlaceholder(BaseDashboardPlaceholder):
    """Aqui se debe editar el numero de filas y columnas, asi como sus dimensiones y rutas de los templates"""

    uid = 'main'
    cols = 15
    rows = 20
    cell_width = 70
    cell_height = 40
    cell_margin_top = 8
    cell_margin_right = 8
    cell_margin_bottom = 8
    cell_margin_left = 8
    edit_template_name = 'bootstrap2/fluid_base_placeholder_edit.html'


class ProductoLayout(BaseDashboardLayout):
    """Layout del Producto."""

    uid = 'producto_layout'
    name = 'Producto Layout'
    view_template_name = 'bootstrap2/fluid_view_layout.html'
    edit_template_name = 'bootstrap2/fluid_edit_layout.html'
    plugin_widgets_template_name_ajax = 'bootstrap2/plugin_widgets_ajax.html'
    form_snippet_template_name = \
        'bootstrap2/snippets/generic_form_snippet.html'
    placeholders = [ProductoMainPlaceholder]
    cell_units = 'px'
    media_css = (
        'bootstrap2/css/bootstrap.css',
        'bootstrap2/css/dash_layout_bootstap2_fluid.css',
        # 'css/dash_solid_borders.css',
    )
    media_js = (
        'bootstrap2/js/bootstrap.js',
        'bootstrap2/js/dash_layout_bootstap2_fluid.js',
    )

    def get_view_template_name(self, request=None, origin=None):
        """Override the master view template for public dashboard app."""
        if origin == 'dash.public_dashboard':
            return 'bootstrap2/fuild_public_dashboard_view_layout.html'
        else:
            return super(ProductoLayout, self).get_view_template_name(
                request=request,
                origin=origin
            )


layout_registry.register(ProductoLayout)
