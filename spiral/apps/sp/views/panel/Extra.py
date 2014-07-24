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

    def get_extras(self, **kwargs):
        return Extras()

    def save_extra(self, project):
        extra = self.extras
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
            extra_detail_model.currency_id = detail.get('currency').get('id')
            extra_detail_model.budget = float(detail.get('budget')) if detail.get('budget') is not None and detail.get('budget') != '' else None
            extra_detail_model.budget_cost = float(detail.get('budget_cost')) if detail.get('budget_cost') is not None and detail.get('budget_cost') != '' else None
            extra_detail_model.schedule = detail.get('schedule')
            extra_detail_model.save()