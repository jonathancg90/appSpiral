# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.panel.Currency import CurrencyDataListView


urlpatterns = patterns('',
                       url(r'^list-json/$',
                           CurrencyDataListView.as_view(),
                           name='currency_list_json'),
                       )