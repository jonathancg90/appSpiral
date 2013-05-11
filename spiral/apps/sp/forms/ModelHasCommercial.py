from django import forms
from apps.sp.models.Entry import Entry
from crispy_forms.helper import FormHelper
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Layout, Field, Button


class ModelHasCommercialForm(forms.Form):

    entry = forms.ChoiceField(
        label=_(u'Rubro'),
        choices=[('', '--------------')],
        required=False
    )
    brand = forms.ChoiceField(
        label=_(u'Marca'),
        choices=[('', '--------------')],
        required=False
    )
    commercial = forms.ChoiceField(
        label=_(u'Comercial'),
        choices=[('', '--------------')],
        required=False
    )
