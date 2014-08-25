from django import forms
from crispy_forms.helper import FormHelper
from apps.sp.models.Client import Client


class ClientFiltersForm(forms.Form):
    name__icontains = forms.CharField(max_length=100,
                                      required=False,
                                      label='Name'
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(ClientFiltersForm, self).__init__(*args, **kwargs)


class ClientForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'nombre'

    class Meta:
        model = Client
        exclude = ['status']