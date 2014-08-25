from django.conf.urls import url, patterns
from apps.sp.views.panel.Commercial import CommercialListView, CommercialCreateView,\
    CommercialUpdateView, CommercialDeleteView, CommercialByBrandIdJson,\
    CommercialDataListView, CommercialCreateDataJson

urlpatterns = patterns('',

     #Commercial
    url(r'^list/$',
        CommercialListView.as_view(),
        name='commercial_list'),
    url(r'^create/$',
        CommercialCreateView.as_view(),
        name='commercial_create'),
    url(r'^edit/(?P<pk>\d+)/$',
        CommercialUpdateView.as_view(),
        name='commercial_edit'),
    url(r'^delete/(?P<pk>\d+)/$',
        CommercialDeleteView.as_view(),
        name='commercial_delete'),
    url(r'^commercial-by-brand/(?P<brand>\d+)/$',
        CommercialByBrandIdJson.as_view(),
        name='commercial_by_brand_json'),
    url(r'^data-list/$',
        CommercialDataListView.as_view(),
        name='commercial_data_list'),
    url(r'^json-create/$',
        CommercialCreateDataJson.as_view(),
        name='commercial_json_create'),
)