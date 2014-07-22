# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns
from apps.sp.views.panel.Employee import EmployeeDataList


urlpatterns = patterns('',
                       #Country
                       url(r'^list-json/$',
                           EmployeeDataList.as_view(),
                           name='employee_list_json'),
                       )