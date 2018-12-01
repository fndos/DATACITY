# -*- encoding: utf-8 -*-

from django import forms

class ImportStyleForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(),label="Importar archivo SLD 1.1.0")
    title = forms.CharField(label=u"Título")