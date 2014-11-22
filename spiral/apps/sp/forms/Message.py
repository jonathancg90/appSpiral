from django import forms
from apps.sp.models.Message import Message
from crispy_forms.helper import FormHelper


class MessageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Titulo'

    class Meta:
        model = Message
        exclude = ['status', 'user']


class MessageFiltersForm(forms.Form):
    name__icontains = forms.CharField(max_length=100,
                                      required=False,
                                      label=(u'Name')
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_show_errors = True
        self.helper.form_tag = False
        super(MessageFiltersForm, self).__init__(*args, **kwargs)