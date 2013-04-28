from django.conf.urls import url, patterns
from django.views.generic import TemplateView

urlpatterns = patterns('',

    #Commercial
    url(r'commercial/$',
        TemplateView.as_view(template_name='base.html'),
        name='commercial_list'),
    url(r'commercial/create/$',
        TemplateView.as_view(template_name='base.html'),
        name='main'),
    url(r'commercial/edit/$',
        TemplateView.as_view(template_name='base.html'),
        name='commercial_edit'),
    url(r'commercial/delete/$',
        TemplateView.as_view(template_name='base.html'),
        name='commercial_delete'),
    )