from django.db.models import FileField
from django.forms import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
import os
from django.core.exceptions import ValidationError
def validate_file_extension_xml(value):
	ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
	valid_extensions = [ '.xml',]
	if not ext.lower() in valid_extensions:
		raise ValidationError(u'Debe Ingresar Archivo XML')

def validate_file_extension_config(value):
	ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
	valid_extensions = [ '.netccfg','.polycfg','.sumocfg']
	if not ext.lower() in valid_extensions:
		raise ValidationError(u'Debe Ingresar Archivo de Configuracion')
