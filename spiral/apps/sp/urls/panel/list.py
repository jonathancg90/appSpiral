# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.panel.List import ListListView, ListCreateView, \
    ListUpdateView, ListDeleteView, DetailListCollaborationView, \
    UserCollaborationDelete, ListDataListView, ListDataSaveView, \
    ListAddModelView, ListModelView, ListDetailView, UserListArchived, \
    UserListActive, ListDetailDelete, ListDetailModelSaveView, \
    ListDetailModelUpdateView, ListDetailModelUpdateAvailableView


urlpatterns = patterns('',

                       #List
                       url(r'^list/$',
                           ListListView.as_view(),
                           name='list_list'),
                       url(r'^create/$',
                           ListCreateView.as_view(),
                           name='list_create'),
                       url(r'^edit/(?P<pk>\d+)/$',
                           ListUpdateView.as_view(),
                           name='list_edit'),
                       url(r'^delete/(?P<pk>\d+)/$',
                           ListDeleteView.as_view(),
                           name='list_delete'),


                       url(r'^archived/(?P<pk>\d+)/$',
                           UserListArchived.as_view(),
                           name='list_archived'),
                       url(r'^active/(?P<pk>\d+)/$',
                           UserListActive.as_view(),
                           name='list_active'),

                       url(r'^collaboration/(?P<pk>\d+)/$',
                           DetailListCollaborationView.as_view(),
                           name='list_collaboration'),

                       url(r'^delete-collaboration/(?P<pk>\d+)/(?P<list_fk>\d+)/?$',
                           UserCollaborationDelete.as_view(),
                           name='list_collaboration_delete'),
                       #Json
                       url(r'^list-json/$',
                           ListDataListView.as_view(),
                           name='list_data_json'),
                       url(r'^save-json/$',
                           ListDataSaveView.as_view(),
                           name='list_save_json'),
                       url(r'^add/list-json/$',
                           ListAddModelView.as_view(),
                           name='add_model_list_save_json'),

                        #List model
                       url(r'^(?P<pk>[^/]+)/list-model/$',
                           ListModelView.as_view(),
                           name='list_model'),

                       url(r'^(?P<pk>\d+)/list-detail/$',
                           ListDetailView.as_view(),
                           name='list_detail'),

                       url(r'^list-detail/(?P<pk>\d+)/delete/$',
                           ListDetailDelete.as_view(),
                           name='list_detail_delete'),

                       url(r'^list/(?P<pk>\d+)save-detail/$',
                           ListDetailModelSaveView.as_view(),
                           name='save_list_detail_model'),

                       url(r'^list/update-detail/(?P<pk>[^/]+)/$',
                           ListDetailModelUpdateView.as_view(),
                           name='update_list_detail_model'),

                       url(r'^list/change-available/$',
                           ListDetailModelUpdateAvailableView.as_view(),
                           name='change_available_detail_list_model'),

                       )