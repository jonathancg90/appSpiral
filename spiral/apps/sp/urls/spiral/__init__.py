from django.conf.urls import patterns, include, url
from apps.sp.views.Home import HomeTemplateView, LoginAuthView,\
    LogoutView

urlpatterns = patterns('',
    url(r'^$', HomeTemplateView.as_view(), name='home'),
    url(r'^login/$', LoginAuthView.as_view(), name='login-user'),
    url(r'^log-out/$', LogoutView.as_view(), name='login-out'),
    url(r'^', include('apps.sp.urls.spiral.brand')),
    url(r'^brand/', include('apps.sp.urls.spiral.brand')),
    url(r'^commercial/', include('apps.sp.urls.spiral.commercial')),
    url(r'^contract/', include('apps.sp.urls.spiral.contract')),
    url(r'^model-has-commercial/', include('apps.sp.urls.spiral.model_has_commercial')),
    url(r'^entry/', include('apps.sp.urls.spiral.entry')),
)
