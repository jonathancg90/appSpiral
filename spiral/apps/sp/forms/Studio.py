from django import forms
from apps.sp.models.Studio import Studio
from crispy_forms.helper import FormHelper


class StudioForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(StudioForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'nombre'

    class Meta:
        model = Studio
        exclude = ['status']
