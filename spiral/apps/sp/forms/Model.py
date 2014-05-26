from django import forms
from apps.sp.models.Model import Model, ModelPhone
from apps.sp.models.ModelCriterionDetail import ModelCriterionDetail
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div


class RegisterModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(RegisterModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Model
        exclude = ['status','model_code','last_visit']


class RegisterModelPhoneForm(forms.Form):

    CHOICES = ModelPhone.CHOICE_OPERATOR
    operators = []
    for line in CHOICES:
        if line[0] != ModelPhone.LANDLINE:
            operators.append(line)

    number_landline = forms.CharField(
        max_length=100,
        required=True,
        label=(u'Telefoni fijo')
    )

    operator = forms.ChoiceField(
        choices=operators,
        required=False,
        label=(u'Operador celular')
    )

    number = forms.CharField(
        max_length=100,
        required=False,
        label=(u'Numero celular')
    )


class RegisterCriterionModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(RegisterCriterionModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ModelCriterionDetail
        exclude = ['model']
