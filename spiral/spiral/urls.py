from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    #Panel de administracion
    url(r'^panel/', include('apps.sp.urls.panel')),

    #Registro de modelos
    url(r'^', include('apps.sp.urls.website.home')),

)
