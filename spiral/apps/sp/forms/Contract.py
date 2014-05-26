from django import forms
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
        exclude = ['status', 'model_has_commercial']


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
        self.set_entry()

    def set_entry(self):
        self.fields['character'].choices = [('', '--------------')] +\
                                         list(Contract.objects.all().values_list('id', 'character'))


