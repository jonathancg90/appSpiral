from django.conf.urls import patterns, include, url
from apps.sp.views.website.Home import HomeTemplateView
from apps.sp.views.website.Home import LoginAuthView
from apps.sp.views.website.Home import LogoutView
from apps.sp.views.panel.Email import EmailListView

urlpatterns = patterns('',
    url(r'^$',
        HomeTemplateView.as_view(),
        name='home'),

    url(r'^login/$',
        LoginAuthView.as_view(),
        name='login'),

    url(r'^logout/$',
        LogoutView.as_view(),
        name='logout'),

    url(r'^email/$',
        EmailListView.as_view(),
        name='email_list'),
)