from django import forms
from apps.sp.models.Brand import Brand
from apps.sp.models.Entry import Entry
from crispy_forms.helper import FormHelper
from django.utils.translation import ugettext_lazy as _
from crispy_forms.layout import Layout, Field, Button


class BrandForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(BrandForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'nombre'
        self.fields['entry'].label = 'Rubro'

    class Meta:
        model = Brand
        exclude = ['status']


class BrandFiltersForm(forms.Form):
    entry_id = forms.ChoiceField(
        label=_(u'Rubro'),
        choices=[('', '--------------')],
        required=False
    )
    name__icontains = forms.CharField(max_length=100,
            required=False,
            label=(u'Name')
        )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(BrandFiltersForm, self).__init__(*args, **kwargs)
        self.set_entry()
        self.fields['entry_id'].widget.attrs.update({'class' : 'form-entry'})

    def set_entry(self):
        self.fields['entry_id'].choices = [('', '--------------')] +\
                                         list(Entry.objects.all().values_list('id', 'name'))
