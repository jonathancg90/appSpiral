from django.conf.urls import patterns, include, url
from apps.sp.views.website.model.model import ModelRegisterCreateView


urlpatterns = patterns('',
    #Register Model
    url(r'^register/$',
        ModelRegisterCreateView.as_view(),
        name='website_model_register'),
)