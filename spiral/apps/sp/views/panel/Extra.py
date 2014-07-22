# -*- coding: utf-8 -*-
from django.views.generic import View

from apps.common.view import LoginRequiredMixin, PermissionRequiredMixin
from apps.common.view import JSONResponseMixin
from apps.sp.models.Extras import ExtrasDetailModel, Extras


class ExtraCharacterDataList(LoginRequiredMixin, PermissionRequiredMixin,
                            JSONResponseMixin, View):

    model = ExtrasDetailModel

    def get_character(self):
        data = []
        characters = ExtrasDetailModel.CHOICE_CHARACTER
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


class ExtraSaveProcess(View):
    data_line = {}
    data_models = {}

    def format_date(self, date):
        return date

    def save_extra(self, project):
        extra = Extras()
        extra.project = project
        extra.save()
        return extra

    def save_detail_model_extra(self, project_line):
        for detail in self.data_models:
            extra_detail_model = ExtrasDetailModel()
            extra_detail_model.extras = project_line
            extra_detail_model.quantity = detail.get('cant')
            extra_detail_model.profile = detail.get('profile')
            extra_detail_model.feature = detail.get('feature')
            extra_detail_model.character = detail.get('character').get('id')
            extra_detail_model.currency = detail.get('currency')
            extra_detail_model.budget = detail.get('budget')
            extra_detail_model.budget_cost = detail.get('budget_cost')
            extra_detail_model.schedule = detail.get('schedule')
            extra_detail_model.save()