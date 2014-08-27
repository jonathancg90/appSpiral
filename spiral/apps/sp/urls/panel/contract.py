# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.panel.Contract import ContractCreateView,\
    ContractDeleteView, ContractListView, ContractUpdateView,\
    ContractTypeDataList, SaveContractTypeJsonView


urlpatterns = patterns('',

    #Contract
    url(r'^model-commercial/(?P<fk>\d+)/list/$',
        ContractListView.as_view(),
        name='contract_list'),
    url(r'^model-commercial/(?P<fk>\d+)/create/$',
        ContractCreateView.as_view(),
        name='contract_create'),
    url(r'^model-commercial/(?P<fk>\d+)/edit/(?P<pk>\d+)/$',
        ContractUpdateView.as_view(),
        name='contract_edit'),
    url(r'^model-commercial/(?P<fk>\d+)/delete/(?P<pk>\d+)/$',
        ContractDeleteView.as_view(),
        name='contract_delete'),
    url(r'^type-contract/$',
        ContractTypeDataList.as_view(),
        name='type_contract_json'),
    url(r'^save-type-contract/$',
        SaveContractTypeJsonView.as_view(),
        name='save_type_contract_json'),
    )