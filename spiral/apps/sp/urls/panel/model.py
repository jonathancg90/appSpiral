# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.panel.Model import ModelCreateView
from apps.sp.views.panel.Model import ModelDataJsonView
from apps.sp.views.panel.Model import PictureModelCreateView
from apps.sp.views.panel.Model import ModelFeatureCreateView
from apps.sp.views.panel.Model import ModelFeatureDeleteView
from apps.sp.views.panel.Model import ModelFeatureUpdateView
from apps.sp.views.panel.Model import ModelUpdateView
from apps.sp.views.panel.Model import ModelSimpleSearchView
from apps.sp.views.panel.Model import ModelControlTemplateView, \
    DeleteImageModelView, QuickModelUpdateView

urlpatterns = patterns('',

     #Retry
    url(r'^model-control/list/$',
        ModelControlTemplateView.as_view(),
        name='panel_model_control_list'),

    url(r'^model-control/save-profile/$',
        ModelCreateView.as_view(),
        name='panel_model_save_profile'),

    url(r'^model-control/update-profile/(?P<pk>[^/]+)/$',
        ModelUpdateView.as_view(),
        name='panel_model_update_profile'),

    url(r'^model-control/quick-update/$',
        QuickModelUpdateView.as_view(),
        name='quick_update_url'),

    url(r'^model-control/save-feature/(?P<pk>[^/]+)/$',
        ModelFeatureCreateView.as_view(),
        name='panel_model_save_feature'),

    url(r'^model-control/update-feature/(?P<pk>[^/]+)/$',
        ModelFeatureUpdateView.as_view(),
        name='panel_model_update_feature'),

    url(r'^model-control/delete-picture/(?P<pk>[^/]+)/$',
        DeleteImageModelView.as_view(),
        name='panel_model_delete_picture'),

    url(r'^model-control/delete-feature/$',
        ModelFeatureDeleteView.as_view(),
        name='panel_model_delete_feature'),

    url(r'^model-control/information/(?P<pk>[^/]+)/$',
        ModelDataJsonView.as_view(),
        name='panel_information_model'),

    url(r'^model-control/save-picture/$',
        PictureModelCreateView.as_view(),
        name='panel_model_save_picture'),

    url(r'^model-control/simple-search/$',
        ModelSimpleSearchView.as_view(),
        name='simple_search_model'),
)