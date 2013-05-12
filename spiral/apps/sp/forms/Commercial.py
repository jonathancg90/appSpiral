from django import forms
from apps.sp.models.Commercial import Commercial
from crispy_forms.helper import FormHelper
from django.utils.translation import ugettext_lazy as _
from apps.sp.models.Entry import Entry
from apps.sp.models.Brand import Brand



class CommercialForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(CommercialForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'comercial'
        self.fields['realized'].label = 'realizado'
        self.fields['brand_id'].label = 'marca'
        self.fields['project'] = forms.CharField(label='project', max_length=9, min_length=9)
        self.Meta.fields.append('project')

    class Meta:
        model = Commercial
        fields = ['name', 'realized', 'brand_id']
        exclude = [ 'status', 'project_id' ]



class CommercialFiltersForm(forms.Form):
    entry_id = forms.ChoiceField(
        label=_(u'Rubro'),
        choices=[('', '--------------')],
        required=False
    )
    brand_id = forms.ChoiceField(
        label=_(u'Marca'),
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
        super(CommercialFiltersForm, self).__init__(*args, **kwargs)
        self.set_entry()

    def set_entry(self):
        self.fields['entry_id'].choices = [('', '--------------')] +\
                                         list(Entry.objects.all().values_list('id', 'name'))

    def set_brand(self):
        self.fields['brand_id'].choices = [('', '--------------')] +\
                                         list(Brand.objects.all().values_list('id', 'name'))