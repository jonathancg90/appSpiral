# -*- coding: utf-8 -*-

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from apps.common.view import SearchFormMixin
from apps.sp.forms.Contract import ContractForm, ContractFiltersForm
from apps.sp.models.Contract import Contract
from apps.sp.models.ModelHasCommercial import ModelHasCommercial
from apps.common.view import LoginRequiredMixin


class ContractCreateView(LoginRequiredMixin, CreateView):
    model = Contract
    form_class = ContractForm
    template_name = 'panel/contract/create.html'
    success_url = 'contract_list'

    def get_context_data(self, **kwargs):
        context = super(ContractCreateView, self).get_context_data(**kwargs)
        context['model_has_commercial'] = get_object_or_404(ModelHasCommercial, id=self.kwargs.get('fk'))
        return context

    def form_valid(self, form):
        value = form.save(commit=False)
        value.model_has_commercial = get_object_or_404(ModelHasCommercial, id=self.kwargs.get('fk', 0))
        return super(ContractCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('contract_list', kwargs={'fk': self.kwargs.get('fk', 0)})


class ContractUpdateView(LoginRequiredMixin, UpdateView):
    model = Contract
    form_class = ContractForm
    template_name = 'panel/contract/update.html'
    success_url = 'contract_list'

    def get_context_data(self, **kwargs):
        context = super(ContractUpdateView, self).get_context_data(**kwargs)
        context['model_has_commercial'] = get_object_or_404(ModelHasCommercial, id=self.kwargs.get('fk'))
        return context

    def get_success_url(self):
        return reverse('contract_list', kwargs={'fk': self.kwargs.get('fk', 0)})


class ContractDeleteView(LoginRequiredMixin, DeleteView):
    model = Contract
    template_name = 'panel/contract/delete.html'
    success_url = 'contract_list'

    def get_context_data(self, **kwargs):
        context = super(ContractDeleteView, self).get_context_data(**kwargs)
        context['model_has_commercial'] = get_object_or_404(ModelHasCommercial, id=self.kwargs.get('fk'))
        return context

    def get_success_url(self):
        return reverse('contract_list', kwargs={'fk': self.kwargs.get('fk', 0)})


class ContractListView(LoginRequiredMixin, SearchFormMixin,ListView):
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

    def get_queryset(self):
        qs = super(ContractListView, self).get_queryset()
        qs =  qs.filter(model_has_commercial_id=self.kwargs.get('fk'))
        return qs
