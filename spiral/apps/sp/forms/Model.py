from django import forms
from apps.sp.models.Model import Model
from django.contrib.auth.models import User
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

    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email already used")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username already used")
        return email