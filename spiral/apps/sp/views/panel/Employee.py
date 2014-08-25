# -*- coding: utf-8 -*-

from django.views.generic import View
from django.db import connections

from apps.common.view import LoginRequiredMixin
from apps.common.view import JSONResponseMixin


class EmployeeDataList(LoginRequiredMixin, JSONResponseMixin, View):
    PRODUCTION_AREA = 2
    REALIZED_AREA = 7
    STATUS_ACTIVE = 1

    def get(self, request, *args, **kwargs):
        context = {}
        context['productors'] = self.get_list_employees(self.PRODUCTION_AREA)
        context['realized'] = self.get_list_employees(self.REALIZED_AREA)
        return self.render_to_response(context)

    def get_list_employees(self, area):
        data = []
        try:
            cursor = connections['employee'].cursor()
            sql = "select idemp, nombres, apellidos from empleado "
            sql += "where idest=%s and idare=%s" %(self.STATUS_ACTIVE, area )
            cursor.execute(sql)
            for row in cursor.fetchall():
                employee = {
                    'id_emp': row[0],
                    'name': row[1],
                    'last_name': row[2]
                }
                data.append(employee)
            return data
        except Exception, e:
            return data
