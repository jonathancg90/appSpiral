from django import forms
from apps.sp.models.Project import Project
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Button



class ProjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(ProjectForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Project
        exclude = ['created', 'modified']


