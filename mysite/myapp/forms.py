from django.forms import ModelForm
from . models import Location,Database
from django import forms

class UserInput(ModelForm):
    class Meta:
        model=Location
        fields=('address','city','state','pincode')


class MyModelForm(forms.ModelForm):
    class Meta:
        model = Database
        fields = '__all__'

