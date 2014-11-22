# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.panel.Message import MessageListView,\
    MessageCreateView, MessageUpdateView, MessageDeleteView, \
    MessageListJsonView, SendMessageJsonView

urlpatterns = patterns('',

                       #List
                       url(r'^list/$',
                           MessageListView.as_view(),
                           name='message_list'),

                       url(r'^create/$',
                           MessageCreateView.as_view(),
                           name='message_create'),

                       url(r'^update/(?P<pk>\d+)/$',
                           MessageUpdateView.as_view(),
                           name='message_edit'),

                       url(r'^delete/(?P<pk>\d+)/$',
                           MessageDeleteView.as_view(),
                           name='message_delete'),

                       url(r'^list-json/$',
                           MessageListJsonView.as_view(),
                           name='message_data_json'),

                       url(r'^send-message/$',
                           SendMessageJsonView.as_view(),
                           name='send_message_data_json'),

                       )