# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.panel.MediaFeature import MediaFeatureListView
from apps.sp.views.panel.MediaFeature import MediaFeatureCreateView
from apps.sp.views.panel.MediaFeature import MediaFeatureUpdateView
from apps.sp.views.panel.MediaFeature import MediaFeatureDeleteView
from apps.sp.views.panel.MediaFeature import MediaFeatureValueListView
from apps.sp.views.panel.MediaFeature import MediaFeatureValueCreateView
from apps.sp.views.panel.MediaFeature import MediaFeatureValueUpdateView
from apps.sp.views.panel.MediaFeature import MediaFeatureValueDeleteView

urlpatterns = patterns('',

                       #MediaFeature
                       url(r'^list/$',
                           MediaFeatureListView.as_view(),
                           name='media_feature_list'),
                       url(r'^create/$',
                           MediaFeatureCreateView.as_view(),
                           name='media_feature_create'),
                       url(r'^edit/(?P<pk>\d+)/$',
                           MediaFeatureUpdateView.as_view(),
                           name='media_feature_edit'),
                       url(r'^delete/(?P<pk>\d+)/$',
                           MediaFeatureDeleteView.as_view(),
                           name='media_feature_delete'),
                        #Media Feature Value

                        url(r'^(?P<pk>\d+)/value/list/$',
                            MediaFeatureValueListView.as_view(),
                            name='media_feature_value_list'),
                        url(r'^(?P<pk>\d+)/value/create/$',
                            MediaFeatureValueCreateView.as_view(),
                            name='media_feature_value_create'),
                        url(r'^value/edit/(?P<pk>\d+)/$',
                            MediaFeatureValueUpdateView.as_view(),
                            name='media_feature_value_edit'),
                        url(r'^value/delete/(?P<pk>\d+)/$',
                            MediaFeatureValueDeleteView.as_view(),
                            name='media_feature_value_delete'),
                       )