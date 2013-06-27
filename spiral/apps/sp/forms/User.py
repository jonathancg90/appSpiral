from django import forms
from crispy_forms.helper import FormHelper
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=_(u'Email')
    )

    password = forms.CharField(
        max_length=60,
        required=True,
        label=_(u'Password'),
        widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(LoginForm, self).__init__(*args, **kwargs)