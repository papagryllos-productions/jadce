"""
Useful django forms
"""

from django import forms
from geoposition.forms import GeopositionField

# a form for the new-event page
class EventForm(forms.Form):
    title = forms.CharField(max_length=100, required=True)
    description = forms.CharField(widget = forms.Textarea, required=False)
    position = GeopositionField()
    photo1 = forms.ImageField(required=False)
    photo2 = forms.ImageField(required=False)
    photo3 = forms.ImageField(required=False)
    photo4 = forms.ImageField(required=False)
