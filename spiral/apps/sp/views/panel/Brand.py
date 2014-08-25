# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from apps.common.view import SearchFormMixin
from apps.common.view import JSONResponseMixin
from apps.sp.forms.Brand import BrandForm, BrandFiltersForm
from apps.sp.models.Brand import Brand
from apps.common.view import LoginRequiredMixin, PermissionRequiredMixin


class BrandListView(LoginRequiredMixin, PermissionRequiredMixin,
                    SearchFormMixin, ListView):
    model = Brand
    template_name = 'panel/brand/brand_list.html'
    search_form_class = BrandFiltersForm
    paginate_by = settings.PANEL_PAGE_SIZE
    filtering = {
        'entry_id': SearchFormMixin.ALL,
        'name': SearchFormMixin.ALL,
    }

    def get_context_data(self, **kwargs):
        context = super(BrandListView, self).get_context_data(**kwargs)
        context['menu'] = 'maintenance'
        return context


class BrandCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'panel/brand/create.html'
    success_url = 'brand_list'
    permissions = {
        "permission": ('sp.add_brand', ),
    }

    def get_context_data(self, **kwargs):
        context = super(BrandCreateView,self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('brand_list')


class BrandUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = 'panel/brand/update.html'
    success_url = 'brand_list'
    permissions = {
        "permission": ('sp.change_brand', ),
    }

    def get_context_data(self, **kwargs):
        context = super(BrandUpdateView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('brand_list')


class BrandDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    model = Brand
    template_name = 'panel/brand/delete.html'
    success_url = 'brand_list'
    permissions = {
        "permission": ('sp.delete_brand', ),
    }

    def get_context_data(self, **kwargs):
        context = super(BrandDeleteView,self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('brand_list')


class BrandByEntryIdJson(LoginRequiredMixin, PermissionRequiredMixin,
                         JSONResponseMixin, ListView):
    model = Brand

    def get_queryset(self):
        entry_id = self.kwargs.get('entry', 0)
        qs = Brand.objects.filter(entry_id=entry_id)
        return qs

    def get_context_data(self, **kwargs):
        data = {}
        brand = self.get_queryset().values('id', 'name')
        data['brand'] = [item for item in brand]
        return data

