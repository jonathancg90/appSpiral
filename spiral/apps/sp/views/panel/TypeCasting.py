# -*- coding: utf-8 -*-
from django.views.generic import View

from apps.common.view import LoginRequiredMixin, PermissionRequiredMixin
from apps.common.view import JSONResponseMixin
from apps.sp.models.Casting import TypeCasting


class TypeCastingDataList(LoginRequiredMixin, PermissionRequiredMixin,
                               JSONResponseMixin, View):

    model = TypeCasting

    def get_types(self):
        data = []
        types = TypeCasting.objects.filter(status=TypeCasting.STATUS_ACTIVE)
        for type in types:
            data.append({
                'id': type.id,
                'name': type.name
            })
        return data

    def get(self, request, *args, **kwargs):
        context = {}
        context['type'] = self.get_types()
        return self.render_to_response(context)