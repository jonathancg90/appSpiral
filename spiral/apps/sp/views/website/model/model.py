# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from apps.sp.forms.Model import RegisterModelForm, RegisterModelPhoneForm
from apps.sp.models.Model import Model


class ModelRegisterCreateView(CreateView):
    model = Model
    form_class = RegisterModelForm
    template_name = 'website/register_model.html'

    def get_success_url(self):
        return reverse('website_model_register')

    def get_context_data(self, **kwargs):
        register_model_phone = RegisterModelPhoneForm()
        context = super(ModelRegisterCreateView, self).get_context_data(**kwargs)
        context['model_phone_form'] = register_model_phone
        return context