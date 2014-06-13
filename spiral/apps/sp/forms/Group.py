from django import forms
from django.contrib.auth.models import Group
from crispy_forms.helper import FormHelper


class GroupForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(GroupForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Group
