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


class ProjectFiltersForm(forms.Form):
    FORMAT_DATE = '%d/%m/%Y'

    line_productions = forms.ChoiceField(
        label='Linea',
        choices=[('', '--------------')],
        required=False
    )

    start_date__gte = forms.DateTimeField(
        input_formats=(FORMAT_DATE,),
        label='De',
        required=False
    )

    finish_date__lte  = forms.DateTimeField(
        input_formats=(FORMAT_DATE,),
        label='Hasta',
        required=False
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(ProjectFiltersForm, self).__init__(*args, **kwargs)
        self.set_lines()
        self.fields['start_date__gte'].widget.attrs.update({'class' : 'date-picker'})
        self.fields['finish_date__lte'].widget.attrs.update({'class' : 'date-picker'})

    def set_lines(self):
        self.fields['line_productions'].choices = [('', '--------------')] + list(Project.CHOICE_LINE)
