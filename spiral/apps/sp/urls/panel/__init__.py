from django.conf.urls import patterns, include, url

from apps.sp.views.panel.Dashboard import DashboardTemplateView

urlpatterns = patterns('',
    url(r'^$',
        DashboardTemplateView.as_view(),
        name='dashboard_view'),
    url(r'^admin/', include('apps.sp.urls.panel.admin')),
    url(r'^brand/', include('apps.sp.urls.panel.brand')),
    url(r'^country/', include('apps.sp.urls.panel.country')),
    url(r'^commercial/', include('apps.sp.urls.panel.commercial')),
    url(r'^contract/', include('apps.sp.urls.panel.contract')),
    url(r'^model-has-commercial/', include('apps.sp.urls.panel.model_has_commercial')),
    url(r'^entry/', include('apps.sp.urls.panel.entry')),
    url(r'^model/', include('apps.sp.urls.panel.model')),
    url(r'^search/', include('apps.sp.urls.panel.search')),
    url(r'^project/', include('apps.sp.urls.panel.project')),
    url(r'^client/', include('apps.sp.urls.panel.client')),
)