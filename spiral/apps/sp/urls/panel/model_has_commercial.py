# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.panel.ModelHasCommercial import ModelHasCommercialListView, \
    ModelHasCommercialAddListView, ModelHasCommercialAddRedirectView, \
    ModelHasCommercialDelRedirectView, ModelHasCommercialListModelView, \
    ModelHasCommercialRedirectView, ExportModelHasCommercialRedirectView


urlpatterns = patterns('',

    #Model has commercial
    url(r'^list/(?P<key>[^/]+)/$',
        ModelHasCommercialListView.as_view(),
        name='model_commercial_list'),

    url(r'^list/(?P<pk>\w+)/export$',
        ExportModelHasCommercialRedirectView.as_view(),
        name='export_model_commercial_list'),

    #Model has commercial
    url(r'^list/model/(?P<pk>\d+)/$',
        ModelHasCommercialListModelView.as_view(),
        name='model_has_commercial_model_list'),

    url(r'^(?P<pk>\d+)/add/$',
        ModelHasCommercialAddListView.as_view(),
        name='model_commercial_create'),

    url(r'^model/(?P<model_id>\d+)/commercial/(?P<commercial_id>\d+)/add/$',
        ModelHasCommercialAddRedirectView.as_view(),
        name='model_commercial_add'),

    url(r'^delete/(?P<pk>\d+)$',
        ModelHasCommercialDelRedirectView.as_view(),
        name='model_has_commercial_delete'),

    url(r'^list-redirect/',
        ModelHasCommercialRedirectView.as_view(),
        name='model_commercial_redirect'),

)