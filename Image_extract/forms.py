from django import forms
from .models import Ext_Image


class ExtImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Ext_Image
        fields = ('Password', 'image2')
    