# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.panel.Model import ModelControlListView, \
    ModelCreateView, ModelDataView, PictureModelCreateView, \
    ModelDataJsonView, ModelFeatureCreateView

urlpatterns = patterns('',

     #Retry
    url(r'^model-control/list/$',
        ModelControlListView.as_view(),
        name='panel_model_control_list'),

    url(r'^model-control/save-profile/$',
        ModelCreateView.as_view(),
        name='panel_model_save_profile'),

    url(r'^model-control/save-feature/(?P<pk>[^/]+)/$',
        ModelFeatureCreateView.as_view(),
        name='panel_model_save_feature'),

    url(r'^model-control/information/(?P<pk>[^/]+)/$',
        ModelDataJsonView.as_view(),
        name='panel_information_model'),

    url(r'^model-control/data/$',
        ModelDataView.as_view(),
        name='panel_model_data'),

    url(r'^model-control/save-picture/$',
        PictureModelCreateView.as_view(),
        name='panel_model_save_picture'),
)