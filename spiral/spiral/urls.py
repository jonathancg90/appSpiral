from django.conf.urls import patterns, include, url



urlpatterns = patterns('',

    url(r'^', include('apps.sp.urls.spiral')),
    url(r'^', include('apps.sp.urls.panel')),
    url(r'^', include('apps.sp.urls.website')),

)
