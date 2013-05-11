from django.conf.urls import url, patterns
from django.views.generic import TemplateView
from apps.sp.views.Commercial import CommercialListView, CommercialCreateView, CommercialUpdateView, CommercialDeleteView

urlpatterns = patterns('',

     #Commercial
    url(r'list/$',
        CommercialListView.as_view(),
        name='commercial_list'),
    url(r'create/$',
        CommercialCreateView.as_view(),
        name='commercial_create'),
    url(r'edit/(?P<pk>\d+)/$',
        CommercialUpdateView.as_view(),
        name='commercial_edit'),
    url(r'delete/(?P<pk>\d+)/$',
        CommercialDeleteView.as_view(),
        name='commercial_delete'),
    )