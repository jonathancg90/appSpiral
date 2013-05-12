# -*- coding: utf-8 -*-
from django.conf import settings

from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from apps.common.view import SearchFormMixin
from apps.sp.forms.Contract import ContractForm, ContractFiltersForm
from apps.sp.models.Contract import Contract


class ContractCreateView(CreateView):
    model = Contract
    form_class = ContractForm
    template_name = 'panel/contract/create.html'
    success_url = 'contract_list'


class ContractUpdateView(UpdateView):
    model = Contract
    form_class = ContractForm
    template_name = 'panel/contract/update.html'
    success_url = 'contract_list'

class ContractDeleteView(DeleteView):
    model = Contract
    template_name = 'panel/contract/update.html'
    success_url = 'contract_list'


class ContractListView(SearchFormMixin,ListView):
    model = Contract
    template_name = 'panel/contract/brand_list.html'
    search_form_class = ContractFiltersForm
    paginate_by = settings.PANEL_PAGE_SIZE
    filtering = {
        'character': SearchFormMixin.ALL,
    }
