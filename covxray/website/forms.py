"""
Website Forms.

Author: Akhil Kokani
"""
from django import forms
from .models import XrayImages

class XrayImageForm(forms.ModelForm):
    class Meta:
        model = XrayImages
        fields = ('xray_scan_img',)