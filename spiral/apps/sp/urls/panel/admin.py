# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.panel.admin.Group import AdminGroupListView, \
    AdminGroupCreateView, AdminGroupEditView, AdminGroupDeleteView

from apps.sp.views.panel.admin.User import AdminUserListView,\
    AdminUserDetailView, AdminUserGroupDeleteView, AdminUserPermissionDetailView, \
    AdminUserCreateView, AdminUserUpdateView, AdminUserChangeStatusRedirectView

from apps.sp.views.panel.admin.Support import AdminSupportListView
from apps.sp.views.panel.admin.Support import AdminSupportReportView
from apps.sp.views.panel.admin.Support import AdminSupportCompleteRedirectView

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


                       url(r'^user/list/create/$',
                           AdminUserCreateView.as_view(),
                           name='admin_user_create'),

                       url(r'^user/list/edit/(?P<pk>\d+)/$',
                           AdminUserUpdateView.as_view(),
                           name='admin_user_update'),

                       url(r'^user/list/edit/(?P<pk>\d+)/status/$',
                           AdminUserChangeStatusRedirectView.as_view(),
                           name='admin_user_change_status'),

                       url(r'^user/(?P<pk>\d+)/detail/group/$',
                           AdminUserDetailView.as_view(),
                           name='admin_user_group_detail'),

                       url(r'^user/(?P<pk>\d+)/detail/permission/$',
                           AdminUserPermissionDetailView.as_view(),
                           name='admin_user_permission_detail'),

                       url(r'^user/(?P<pk>\d+)/detail/group/delete/$',
                           AdminUserGroupDeleteView.as_view(),
                           name='admin_user_group_delete'),

                    #Support
                       url(r'^user/support/$',
                           AdminSupportListView.as_view(),
                           name='admin_user_support_list'),

                       url(r'^user/support/save/$',
                           AdminSupportReportView.as_view(),
                           name='admin_user_support_save'),

                       url(r'^user/support/complete/(?P<pk>\d+)/$',
                           AdminSupportCompleteRedirectView.as_view(),
                           name='admin_user_support_complete'),
)
