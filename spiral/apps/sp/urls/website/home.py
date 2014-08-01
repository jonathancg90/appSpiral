from django.conf.urls import patterns, include, url
from apps.sp.views.website.Home import HomeFormView
from apps.sp.views.website.Home import LoginAuthView
from apps.sp.views.website.Home import LogoutView
from apps.sp.views.website.Home import RecoverPasswordFormView
from apps.sp.views.website.Home import RegisterUser
from apps.sp.views.website.Home import LoginMobile
from apps.sp.views.panel.Email import EmailListView

urlpatterns = patterns('',
    url(r'^$',
        HomeFormView.as_view(),
        name='home'),

    url(r'^login/$',
        LoginAuthView.as_view(),
        name='login'),

    url(r'^login-mobil/$',
        LoginMobile.as_view(),
        name='login_mobile'),

    url(r'^logout/$',
        LogoutView.as_view(),
        name='logout'),

    url(r'^register/$',
        RegisterUser.as_view(),
        name='register_user'),

    url(r'^email/$',
        EmailListView.as_view(),
        name='email_list'),

    url(r'^recover/$',
        RecoverPasswordFormView.as_view(),
        name='recover_password')
)