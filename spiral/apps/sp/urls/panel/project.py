# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.panel.Project import ProjectListView,\
    ProjectCreateView, ProjectRolesJsonView, ProjectSaveJsonView, \
    ProjectLinesJsonView, ProjectUpdateJsonView, ProjectDataUpdateJsonView, \
    DetailModelJsonView, ProjectFinishRedirectView, ProjectStartRedirectView, \
    ProjectDeleteRedirectView

urlpatterns = patterns('',
                       url(r'^$',
                           ProjectListView.as_view(),
                           name='project_list'),

                       url(r'^update-finish/(?P<pk>\d+)/$',
                           ProjectFinishRedirectView.as_view(),
                           name='project_change_finish'),

                       url(r'^update-start/(?P<pk>\d+)/$',
                           ProjectStartRedirectView.as_view(),
                           name='project_change_start'),

                       url(r'^delete/(?P<pk>\d+)/$',
                           ProjectDeleteRedirectView.as_view(),
                           name='project_delete'),

                       url(r'^create/(?P<pk>[^/]+)/$',
                           ProjectCreateView.as_view(),
                           name='project_crud'),

                       url(r'^roles/$',
                           ProjectRolesJsonView.as_view(),
                           name='project_roles_json'),

                       url(r'^save/$',
                           ProjectSaveJsonView.as_view(),
                           name='project_save'),

                       url(r'^update/$',
                           ProjectUpdateJsonView.as_view(),
                           name='project_update'),

                       url(r'^data-update/(?P<pk>[^/]+)/$',
                           ProjectDataUpdateJsonView.as_view(),
                           name='project_update_data_json'),

                       url(r'^line-json/$',
                           ProjectLinesJsonView.as_view(),
                           name='project_line_json'),

                       url(r'^detail-model-json/(?P<pk>[^/]+)/$',
                           DetailModelJsonView.as_view(),
                           name='detail_model_json'),
                       )
