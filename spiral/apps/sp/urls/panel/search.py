# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.panel.search.CommercialRealized import CommercialRealizedListView


urlpatterns = patterns('',

    #Model has commercial
    url(r'^commercial-realized/$',
        CommercialRealizedListView.as_view(),
        name='search_commercial_realized'),

)