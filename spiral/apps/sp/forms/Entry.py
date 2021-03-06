from django import forms
from apps.sp.models.Entry import Entry
from crispy_forms.helper import FormHelper


class EntryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(EntryForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'nombre'

    class Meta:
        model = Entry
        exclude = [ 'status']


class EntryFiltersForm(forms.Form):
    name__icontains = forms.CharField(max_length=100,
            required=False,
            label=(u'Name')
        )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(EntryFiltersForm, self).__init__(*args, **kwargs)