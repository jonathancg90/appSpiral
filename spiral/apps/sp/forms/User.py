# -*- coding: utf-8 -*-

from crispy_forms.layout import Field
from django import forms
from crispy_forms.helper import FormHelper, Layout
from django.contrib.auth.models import Group


class LoginForm(forms.Form):
    username = forms.CharField(
        required=None,
        label='',
    )

    password = forms.CharField(
        max_length=60,
        required=True,
        label='',
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('username', css_class="span12", placeholder="Username", template='helpers/input_login.html'),
            Field('password', css_class="span12", placeholder="Password", template='helpers/input_login.html'),
            )
        super(LoginForm, self).__init__(*args, **kwargs)


class RecoverForm(forms.Form):
    password = forms.CharField(
        max_length=60,
        required=True,
        label='',
        widget=forms.PasswordInput,
    )

    re_password = forms.CharField(
        max_length=60,
        required=True,
        label='',
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('password', css_class="span12", placeholder="Password", template='helpers/input_login.html'),
            Field('re_password', css_class="span12", placeholder="Re Password", template='helpers/input_login.html'),
            )
        super(RecoverForm, self).__init__(*args, **kwargs)

    def clean(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')

        if password and password != re_password:
            raise forms.ValidationError("Contraseñas no coinciden")

        return self.cleaned_data


class UserGroupForm(forms.Form):
    group = forms.ModelChoiceField(
        label='Group',
        queryset=None
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(UserGroupForm, self).__init__(*args, **kwargs)

    def set_groups(self):
        self.fields['group'].queryset = Group.objects.all()
