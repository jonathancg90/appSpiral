from django import forms
from apps.sp.models.Commercial import Commercial
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Button



class CommercialForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(CommercialForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'comercial'
        self.fields['realized'].label = 'realizado'
        self.fields['brand_id'].label = 'marca'
        self.fields['project_id'].label = 'proyecto'

    class Meta:
        model = Commercial
        exclude = [ 'status']


class CommercialFiltersForm(forms.Form):
    name__icontains = forms.CharField(max_length=100,
            required=False,
            label=(u'Name')
        )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(CommercialFiltersForm, self).__init__(*args, **kwargs)

