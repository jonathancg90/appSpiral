# -*- coding: utf-8 -*-

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from apps.common.view import SearchFormMixin
from apps.sp.forms.Contract import ContractForm, ContractFiltersForm
from apps.sp.models.Contract import Contract
from apps.sp.models.ModelHasCommercial import ModelHasCommercial


class ContractCreateView(CreateView):
    model = Contract
    form_class = ContractForm
    template_name = 'panel/contract/create.html'
    success_url = 'contract_list'

    def get_context_data(self, **kwargs):
        context = super(ContractCreateView, self).get_context_data(**kwargs)
        context['model_has_commercial'] = get_object_or_404(ModelHasCommercial, id=self.kwargs.get('fk'))
        return context


class ContractUpdateView(UpdateView):
    model = Contract
    form_class = ContractForm
    template_name = 'panel/contract/update.html'
    success_url = 'contract_list'

    def get_context_data(self, **kwargs):
        context = super(ContractUpdateView, self).get_context_data(**kwargs)
        context['model_has_commercial'] = get_object_or_404(ModelHasCommercial, id=self.kwargs.get('fk'))
        return context


class ContractDeleteView(DeleteView):
    model = Contract
    template_name = 'panel/contract/update.html'
    success_url = 'contract_list'

    def get_context_data(self, **kwargs):
        context = super(ContractDeleteView, self).get_context_data(**kwargs)
        context['model_has_commercial'] = get_object_or_404(ModelHasCommercial, id=self.kwargs.get('fk'))
        return context


class ContractListView(SearchFormMixin,ListView):
    model = Contract
    template_name = 'panel/contract/contract_list.html'
    search_form_class = ContractFiltersForm
    paginate_by = settings.PANEL_PAGE_SIZE
    filtering = {
        'character': SearchFormMixin.ALL,
    }

    def get_context_data(self, **kwargs):
        context = super(ContractListView, self).get_context_data(**kwargs)
        context['model_has_commercial'] = get_object_or_404(ModelHasCommercial, id=self.kwargs.get('fk'))
        return context
