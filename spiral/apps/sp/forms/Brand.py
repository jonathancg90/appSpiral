from django import forms
from apps.sp.models.Brand import Brand
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Button


class BrandForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(BrandForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'nombre'
        self.fields['entry_id'].label = 'marca'

    class Meta:
        model = Brand
        exclude = ['created', 'modified', 'status']


class BrandFiltersForm(forms.Form):
    name__icontains = forms.CharField(max_length=100,
            required=False,
            label=(u'Name')
        )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(BrandFiltersForm, self).__init__(*args, **kwargs)
