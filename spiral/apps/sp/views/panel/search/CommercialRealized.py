# -*- coding: utf-8 -*-

from django.conf import settings
from django.views.generic import ListView
from apps.common.view import  SearchFormMixin
from apps.common.view import LoginRequiredMixin
from apps.sp.models.ModelHasCommercial import ModelHasCommercial
from apps.sp.forms.ModelHasCommercial import ModelHasCommercialFilterForm


class CommercialRealizedListView(LoginRequiredMixin, SearchFormMixin, ListView):
    template_name = 'panel/search/commercial_realized.html'
    model = ModelHasCommercial
    context_object_name = 'search_commercial_realized'
    search_form_class = ModelHasCommercialFilterForm
    paginate_by = settings.PANEL_PAGE_SIZE
    filtering = {
        'commercial_id': SearchFormMixin.ALL,
        'commercial__brand': SearchFormMixin.ALL,
        'commercial__brand__entry': SearchFormMixin.ALL,
        'commercial_realized__iexact': SearchFormMixin.ALL,
    }

    def get_queryset(self):
        qs = super(CommercialRealizedListView, self).get_queryset()
        qs = self._set_filter_brand(qs)
        qs = self._set_filter_entry(qs)
        return qs

    def _set_filter_entry(self, qs):
        entry_id = str(self.request.GET.get('commercial__brand__entry', None))
        if entry_id.isdigit():
            qs = qs.filter(commercial__brand__entry=entry_id)
        return qs

    def _set_filter_brand(self, qs):
        brand_id = str(self.request.GET.get('commercial__brand', ))
        if brand_id.isdigit():
            qs = qs.filter(commercial__brand=brand_id)
        return qs

    def get_search_form(self, form_class):
        brand_id = self.request.GET.get('commercial__brand', None)
        entry_id = self.request.GET.get('commercial__brand__entry', None)
        form = super(CommercialRealizedListView, self).get_search_form(form_class)
        if brand_id:
            form.set_commercial(brand_id)
        if entry_id:
            form.set_brand(entry_id)
        return form