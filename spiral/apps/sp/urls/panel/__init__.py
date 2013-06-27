from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^brand/', include('apps.sp.urls.panel.brand')),
    url(r'^commercial/', include('apps.sp.urls.panel.commercial')),
    url(r'^contract/', include('apps.sp.urls.panel.contract')),
    url(r'^model-has-commercial/', include('apps.sp.urls.panel.model_has_commercial')),
    url(r'^entry/', include('apps.sp.urls.panel.entry')),
    url(r'^model/', include('apps.sp.urls.panel.model')),
)