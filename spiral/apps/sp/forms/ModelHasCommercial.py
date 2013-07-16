from django import forms
from apps.sp.models.Entry import Entry
from crispy_forms.helper import FormHelper
from django.utils.translation import ugettext_lazy as _
from apps.sp.models.Brand import Brand
from apps.sp.models.Commercial import Commercial


class ModelHasCommercialFilterForm(forms.Form):

    commercial__brand__entry = forms.ChoiceField(
        label=_(u'Rubro'),
        choices=[('', '--------------')],
        required=False
    )
    commercial__brand = forms.ChoiceField(
        label=_(u'Marca'),
        choices=[('', '--------------')],
        required=False
    )
    commercial_id = forms.ChoiceField(
        label=_(u'Comercial'),
        choices=[('', '--------------')],
        required=False
    )
    # commercial_realized__iexact = forms.CharField(
    #     max_length=100,
    #     required=False,
    #     label=_(u'Realizado')
    # )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(ModelHasCommercialFilterForm, self).__init__(*args, **kwargs)
        self.set_entry()
        self.fields['commercial__brand__entry'].widget.attrs.update({'class' : 'form-entry'})
        self.fields['commercial__brand'].widget.attrs.update({'class' : 'form-brand'})
        self.fields['commercial_id'].widget.attrs.update({'class' : 'form-commercial'})

    def set_entry(self):
        self.fields['commercial__brand__entry'].choices = [('', '--------------')] +\
                                         list(Entry.objects.all().values_list('id', 'name'))

    def set_brand(self, entry_id):
        self.fields['commercial__brand'].choices = [('', '--------------')] +list(Brand.objects.filter(
                                            entry=entry_id).values_list('id', 'name'))

    def set_commercial(self, brand_id):
        self.fields['commercial_id'].choices = [('', '--------------')] +list(Commercial.objects.filter(
                                            brand=brand_id).values_list('id', 'name'))
