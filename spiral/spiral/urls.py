from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('',
    #Panel de administracion
    url(r'^panel/', include('apps.sp.urls.panel')),

    #Registro de modelos
    url(r'^', include('apps.sp.urls.website.home')),

    # url(r'^$', lambda x: HttpResponseRedirect('/upload/new/')),
    url(r'^upload/', include('apps.fileupload.urls')),
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT}))