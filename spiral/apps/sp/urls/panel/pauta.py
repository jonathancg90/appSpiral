# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.panel.Pauta import PautaTemplateView, \
    PautaProjectListJsonView, PautaAddModelJsonView, PautaListJsonView, DetailPautaStatusUpdate

urlpatterns = patterns('',

                       #Pauta
                       url(r'^list/$',
                           PautaTemplateView.as_view(),
                           name='pauta_list'),

                       url(r'^list-json/$',
                           PautaListJsonView.as_view(),
                           name='pauta_list_json'),

                       url(r'^project-pauta/$',
                           PautaProjectListJsonView.as_view(),
                           name='project_pauta_list'),

                       url(r'^add-pauta/$',
                           PautaAddModelJsonView.as_view(),
                           name='project_pauta_add'),

                       url(r'^update-pauta/status/$',
                           DetailPautaStatusUpdate.as_view(),
                           name='pauta_status_update_json'),

                       )