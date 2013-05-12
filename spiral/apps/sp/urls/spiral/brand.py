# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.Brand import BrandListView, BrandCreateView,\
    BrandUpdateView, BrandDeleteView, BrandByEntryIdJson


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
    url(r'brand-by-entry/(?P<entry>\d+)/$',
        BrandByEntryIdJson.as_view(),
        name='brand_by_entry_json'),

)