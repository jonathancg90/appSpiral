# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.panel.search.CommercialRealized import CommercialRealizedListView, \
    ModelsPerCommercial, ExportCommercialRealizedView, ModelSearchView, ModelBasicSearchView,\
    ModelAdvanceSearchView


urlpatterns = patterns('',

    url(r'^commercial-realized/$',
        CommercialRealizedListView.as_view(),
        name='search_commercial_realized'),

    url(r'^models-per-commercial/$',
        ModelsPerCommercial.as_view(),
        name='search_models_per_comercial'),

    url(r'^models-per-commercial/export/(?P<pk>\d+)/$',
        ExportCommercialRealizedView.as_view(),
        name='search_export_models_per_comercial'),

    url(r'^models/$',
        ModelSearchView.as_view(),
        name='search_model'),

    url(r'^models/basic-search/$',
        ModelBasicSearchView.as_view(),
        name='search_basic_model'),

    url(r'^models/advance-search/$',
        ModelAdvanceSearchView.as_view(),
        name='search_advance_model'),


)