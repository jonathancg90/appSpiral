from django import forms
from apps.sp.models.PictureDetail import MediaFeature, MediaFeatureValue
from crispy_forms.helper import FormHelper


class MediaFeatureForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(MediaFeatureForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'nombre'

    class Meta:
        model = MediaFeature
        exclude = ['status']


class MediaFeatureFiltersForm(forms.Form):

    name__icontains = forms.CharField(max_length=100,
            required=False,
            label=(u'Name')
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(MediaFeatureFiltersForm, self).__init__(*args, **kwargs)


class MediaFeatureValueForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(MediaFeatureValueForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'nombre'

    def set_media_feature(self, media_feature):
        self.fields['media_feature'].choices = [(media_feature.id, media_feature.name)] + list(MediaFeature.objects.exclude(
            pk=media_feature.id).values_list('id', 'name'))

    class Meta:
        model = MediaFeatureValue
        exclude = ['status']


class MediaFeatureValueFiltersForm(forms.Form):

    name__icontains = forms.CharField(max_length=100,
                                      required=False,
                                      label=(u'Name')
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(MediaFeatureValueFiltersForm, self).__init__(*args, **kwargs)
