# -*- coding: utf-8 -*-
from django.views.generic import View

from apps.common.view import LoginRequiredMixin, PermissionRequiredMixin
from apps.common.view import JSONResponseMixin
from apps.sp.models.Casting import Casting, CastingDetailModel, TypeCasting


class CastingCharacterDataList(LoginRequiredMixin, PermissionRequiredMixin,
                               JSONResponseMixin, View):

    model = CastingDetailModel

    def get_character(self):
        data = []
        characters = CastingDetailModel.CHOICE_CHARACTER
        for character in characters:
            data.append({
                'id': character[0],
                'name': character[1]
            })
        return data

    def get(self, request, *args, **kwargs):
        context = {}
        context['character'] = self.get_character()
        return self.render_to_response(context)


class CastingSaveProcess(View):
    data_line = {}
    data_models = {}

    def format_date(self, date):
        return date

    def get_casting(self, **kwargs):
        return Casting()

    def save_casting(self, project):
        casting = self.casting
        casting.project = project
        casting.ppi = self.format_date(self.data_line.get('ppi'))
        casting.ppg = self.format_date(self.data_line.get('ppg'))
        casting.realized = self.format_date(self.data_line.get('realized'))
        casting.save()
        casting.type_casting.clear()
        for type in self.data_line.get('type_casting', []):
            casting.type_casting.add(TypeCasting.objects.get(pk=type.get('id')))

        return casting

    def save_detail_model_casting(self, project_line):
        for detail in self.data_models:
            casting_detail_model = CastingDetailModel()
            casting_detail_model.casting = project_line
            casting_detail_model.quantity = detail.get('cant')
            casting_detail_model.profile = detail.get('profile')
            casting_detail_model.feature = detail.get('feature')
            casting_detail_model.character = detail.get('character').get('id')
            casting_detail_model.scene = detail.get('scene')
            casting_detail_model.budget = float(detail.get('budget')) if detail.get('budget') is not None and detail.get('budget') != '' else None
            casting_detail_model.save()
            casting_detail_model.type_casting.clear()
            for type in detail.get('type'):
                type_casting = TypeCasting.objects.get(pk=type.get('id'))
                casting_detail_model.type_casting.add(type_casting)