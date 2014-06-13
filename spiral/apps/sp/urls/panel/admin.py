# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.panel.admin.Group import AdminGroupListView, \
    AdminGroupCreateView, AdminGroupEditView, AdminGroupDeleteView
from apps.sp.views.panel.admin.User import AdminUserListView,\
    AdminUserDetailView, AdminUserGroupDeleteView
from apps.sp.views.panel.Dashboard import SettingsTemplateView

urlpatterns = patterns('',
                       url(r'^settings/$',
                           SettingsTemplateView.as_view(),
                           name='admin_settings'),

                       #Group
                       url(r'^group/list/$',
                           AdminGroupListView.as_view(),
                           name='admin_group_list'),
                       
                       url(r'^group/create/$',
                           AdminGroupCreateView.as_view(),
                           name='admin_group_create'),

                       url(r'^group/edit/(?P<pk>\d+)/$',
                           AdminGroupEditView.as_view(),
                           name='admin_group_edit'),
                       url(r'^group/delete/$',
                           AdminGroupDeleteView.as_view(),
                           name='admin_group_delete'),

                       #User
                       url(r'^user/list/$',
                           AdminUserListView.as_view(),
                           name='admin_user_list'),

                       url(r'^user/(?P<pk>\d+)/detail/group/$',
                           AdminUserDetailView.as_view(),
                           name='admin_user_group_detail'),

                       url(r'^user/(?P<pk>\d+)/detail/group/delete/$',
                           AdminUserGroupDeleteView.as_view(),
                           name='admin_user_group_delete'),
)
