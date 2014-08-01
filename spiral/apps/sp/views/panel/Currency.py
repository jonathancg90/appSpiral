# -*- coding: utf-8 -*-

from django.views.generic import ListView
from apps.sp.models.Currency import Currency
from apps.common.view import JSONResponseMixin
from apps.common.view import LoginRequiredMixin, PermissionRequiredMixin


class CurrencyDataListView(LoginRequiredMixin, PermissionRequiredMixin,
                        JSONResponseMixin, ListView):
    model = Currency

    def get_queryset(self):
        qs = Currency.objects.filter(status=Currency.STATUS_ACTIVE)
        return qs

    def get_context_data(self, **kwargs):
        data = {}
        coins = self.get_queryset().values('id', 'symbol')
        data['currency'] = [item for item in coins]
        return data