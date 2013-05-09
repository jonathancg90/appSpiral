# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.ModelHasCommercial import ModelHasCommercialListView, \
    ModelHasCommercialAddListView, ModelHasCommercialAddRedirectView, \
    ModelHasCommercialDelRedirectView, ModelHasCommercialListModelView



urlpatterns = patterns('',

    #Model has commercial
    url(r'^list/(?P<key>\w+)/$',
        ModelHasCommercialListView.as_view(),
        name='model_commercial_list'),

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

)