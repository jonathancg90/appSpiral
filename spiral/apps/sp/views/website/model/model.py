# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from apps.sp.forms.Brand import BrandForm, BrandFiltersForm
from apps.sp.models.Model import Model


class BrandCreateView(CreateView):
    model = Model
    form_class = BrandForm
    template_name = 'panel/brand/create.html'
    success_url = 'brand_list'

    def get_context_data(self, **kwargs):
        context = super(BrandCreateView,self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('brand_list')