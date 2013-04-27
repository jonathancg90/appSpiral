from django import forms
from apps.sp.models.Contract import Contract
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Button



class ContractForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(ContractForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Contract
        exclude = [ 'created', 'modified', 'status', 'model_has_contract']


