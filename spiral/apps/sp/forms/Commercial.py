from django import forms
from apps.sp.models.Commercial import Commercial
from crispy_forms.helper import FormHelper
from django.utils.translation import ugettext_lazy as _
from apps.sp.models.Entry import Entry
from apps.sp.models.Brand import Brand


class CommercialCreateForm(forms.ModelForm):

    entry_id = forms.ChoiceField(
        label=_(u'Rubro'),
        choices=[('', '--------------')],
        required=False
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(CommercialCreateForm, self).__init__(*args, **kwargs)
        self.fields['project'] = forms.CharField(
            label='Codigo del proyecto',
            max_length=9,
            min_length=9,
            required=False
        )
        self.Meta.fields.append('project')
        self.set_entry()
        self.fields['entry_id'].widget.attrs.update({'class' : 'form-entry'})
        self.fields['brand'].widget.attrs.update({'class' : 'form-brand'})
        self.fields['brand'].choices = [('', '--------------')]
        self.fields.keyOrder = ['name', 'realized','entry_id', 'brand', 'project']

    def set_entry(self):
        self.fields['entry_id'].choices = [('', '--------------')] +\
                                         list(Entry.objects.all().values_list('id', 'name'))

    class Meta:
        model = Commercial
        fields = ['name', 'realized', 'brand']
        exclude = ['status', 'project']


class CommercialUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(CommercialUpdateForm, self).__init__(*args, **kwargs)
        self.fields['project'] = forms.CharField(
            label='Codigo del proyecto',
            max_length=9,
            min_length=9
        )
        self.Meta.fields.append('project')


    class Meta:
        model = Commercial
        fields = ['name', 'realized', 'brand']
        exclude = [ 'status', 'project' ]


class CommercialFiltersForm(forms.Form):
    brand__entry = forms.ChoiceField(
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
        self.fields['brand__entry'].widget.attrs.update({'class' : 'form-entry'})
        self.fields['brand_id'].widget.attrs.update({'class' : 'form-brand'})

    def set_entry(self):
        self.fields['brand__entry'].choices = [('', '--------------')] +\
                                         list(Entry.objects.all().values_list('id', 'name'))

    def set_brand(self, entry_id):
        self.fields['brand_id'].choices = [('', '--------------')] +list(Brand.objects.filter(
                                            entry=entry_id).values_list('id', 'name'))

