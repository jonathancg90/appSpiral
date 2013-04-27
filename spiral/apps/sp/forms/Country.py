from django import forms
from apps.sp.models.Country import Country
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Button



class CountryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(CountryForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Country
        exclude = ['created', 'modified', 'status']


