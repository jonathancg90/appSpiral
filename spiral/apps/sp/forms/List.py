from django import forms
from django.contrib.auth.models import User

from apps.sp.models.List import List
from apps.sp.models.Entry import Entry
from crispy_forms.helper import FormHelper
from django.utils.translation import ugettext_lazy as _


class ListForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(ListForm, self).__init__(*args, **kwargs)
        self.fields['project'].required = False
        self.fields['description'].required = False

    class Meta:
        model = List
        exclude = ['status', 'collaboration']


class ListFiltersForm(forms.Form):
    title__icontains = forms.CharField(max_length=100,
                                      required=False,
                                      label=(u'Name')
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(ListFiltersForm, self).__init__(*args, **kwargs)


class CollaborationForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.none(),
        label=_(u'Usuarios'),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(CollaborationForm, self).__init__(*args, **kwargs)

    def set_users(self, users=None):
        qs = User.objects.filter(
            is_superuser=False
        )
        if users is not None:
            qs = qs.exclude(pk__in=users)
        self.fields['user'].queryset = qs