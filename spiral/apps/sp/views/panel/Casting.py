# -*- coding: utf-8 -*-
from django.views.generic import View

from apps.common.view import LoginRequiredMixin, PermissionRequiredMixin
from apps.common.view import JSONResponseMixin
from apps.sp.models.Casting import CastingDetailModel


class CastingCharacterDataList(LoginRequiredMixin, PermissionRequiredMixin,
                               JSONResponseMixin, View):

    model = CastingDetailModel

    def get_character(self):
        data = []
        characters = CastingDetailModel.CHOICE_CHARACTER
        for character in characters:
            data.append(character[1])
        return data

    def get(self, request, *args, **kwargs):
        context = {}
        context['character'] = self.get_character()
        return self.render_to_response(context)