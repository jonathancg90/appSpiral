# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.Contract import ContractCreateView, ContractDeleteView, ContractListView, ContractUpdateView


urlpatterns = patterns('',

    #Contract
    url(r'contract/$',
        ContractListView.as_view(),
        name='contract_list'),
    url(r'create/$',
        ContractCreateView.as_view(),
        name='contract_create'),
    url(r'edit/(?P<pk>\d+)/$',
        ContractUpdateView.as_view(),
        name='contract_edit'),
    url(r'delete/(?P<pk>\d+)/$',
        ContractDeleteView.as_view(),
        name='contract_delete'),
    )