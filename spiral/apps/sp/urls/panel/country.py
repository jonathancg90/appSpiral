# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.panel.Country import CountryJsonView


urlpatterns = patterns('',
                       #Country
                       url(r'^list-json/$',
                           CountryJsonView.as_view(),
                           name='country_list_json'),
                       )