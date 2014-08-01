# -*- coding: utf-8 -*-
from django.views.generic import View
from apps.common.view import JSONResponseMixin
from apps.sp.models.Broadcast import Broadcast
from apps.sp.models.Brand import Brand
from apps.common.view import LoginRequiredMixin, PermissionRequiredMixin


class BroadcastJsonView(LoginRequiredMixin, PermissionRequiredMixin,
                        JSONResponseMixin, View):
    model = Broadcast

    def get_broadcasts(self):
        data = []
        broadcasts = Broadcast.objects.filter(status=Broadcast.STATUS_ACTIVE)
        for broadcasts in broadcasts:
            data.append({
                'id': broadcasts.id,
                'name': broadcasts.name
            })
        return data

    def get(self, request, *args, **kwargs):
        context = {}
        context['broadcasts'] = self.get_broadcasts()
        return self.render_to_response(context)


