from django import forms
from .models import Sessions


class SessionForm(forms.ModelForm):
    class Meta:
        model = Sessions
        opening_date = forms.DateTimeField(widget= forms.SelectDateWidget, input_formats=['%Y/%m/%d %H:%M'])
        closing_date = forms.DateTimeField(widget= forms.SelectDateWidget, input_formats=['%Y/%m/%d %H:%M'])
        exclude = ['id']


