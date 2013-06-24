from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    url(r'^', include('apps.sp.urls.spiral')),

    #Panel de administracion
    url(r'^panel/', include('apps.sp.urls.panel')),

    #Registro de modelos
    url(r'^', include('apps.sp.urls.website.register_model')),

)
