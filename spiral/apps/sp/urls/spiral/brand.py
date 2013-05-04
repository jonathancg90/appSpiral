# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from django.views.generic import TemplateView
from apps.sp.views.Brand import BrandListView, BrandCreateView, BrandUpdateView, BrandDeleteView


urlpatterns = patterns('',

     #Brand
    url(r'list/$',
        BrandListView.as_view(),
        name='brand_list'),
    url(r'create/$',
        BrandCreateView.as_view(),
        name='brand_create'),
    url(r'edit/(?P<pk>\d+)/$',
        BrandUpdateView.as_view(),
        name='brand_edit'),
    url(r'delete/(?P<pk>\d+)/$',
        BrandDeleteView.as_view(),
        name='brand_delete'),
)