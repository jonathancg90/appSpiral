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
        exclude = [ 'created', 'modified', 'status']


class ContractFiltersForm(forms.Form):
    entry_id = forms.ChoiceField(
        label=_(u'Rubro'),
        choices=[('', '--------------')],
        required=False
    )
    name__icontains = forms.CharField(max_length=100,
            required=False,
            label=(u'Name')
        )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(ContractFiltersForm, self).__init__(*args, **kwargs)
        self.set_entry()

    def set_entry(self):
        self.fields['entry_id'].choices = [('', '--------------')] +\
                                         list(Contract.objects.all().values_list('id', 'name'))


