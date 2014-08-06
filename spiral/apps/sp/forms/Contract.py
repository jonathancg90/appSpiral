from django import forms
from crispy_forms.layout import  Layout, Div
from crispy_forms.bootstrap import Field
from apps.sp.models.Contract import Contract
from crispy_forms.helper import FormHelper
from django.utils.translation import ugettext_lazy as _


class ContractForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(ContractForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Contract
        exclude = ['status']


class ContractFiltersForm(forms.Form):
    character = forms.ChoiceField(
        label=_(u'Personaje'),
        choices=[('', '--------------')],
        required=False
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(ContractFiltersForm, self).__init__(*args, **kwargs)


