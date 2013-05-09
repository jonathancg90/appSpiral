from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    url(r'^brand/', include('apps.sp.urls.spiral.brand')),
    url(r'^commercial/', include('apps.sp.urls.spiral.commercial')),
    url(r'^contract/', include('apps.sp.urls.spiral.contract')),
    url(r'^model-has-commercial/', include('apps.sp.urls.spiral.model_has_commercial')),
    url(r'^entry/', include('apps.sp.urls.spiral.entry')),
)
