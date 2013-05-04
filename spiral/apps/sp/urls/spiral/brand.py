# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from django.views.generic import TemplateView
from apps.sp.views.Brand import BrandListView, BrandCreateView, BrandUpdateView, BrandDeleteView


urlpatterns = patterns('',

     #Brand
    url(r'list/$',
        BrandListView.ad_view(),
        name='brand_list'),
    url(r'create/$',
        BrandCreateView.as_view(),
        name='brand_create'),
    url(r'edit/$',
        BrandUpdateView.as_view(),
        name='brand_edit'),
    url(r'delete/$',
        BrandDeleteView.as_view(),
        name='brand_delete'),
)