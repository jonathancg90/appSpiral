# -*- coding: utf-8 -*-
from django.views.generic import View

from apps.common.view import LoginRequiredMixin, PermissionRequiredMixin
from apps.common.view import JSONResponseMixin
from apps.sp.models.Representation import TypeEvent, \
    RepresentationDetailModel, Representation


class RepresentationEventsDataList(LoginRequiredMixin, PermissionRequiredMixin,
                               JSONResponseMixin, View):

    model = TypeEvent

    def get_type_events(self):
        data = []
        events = TypeEvent.objects.filter(status=TypeEvent.STATUS_ACTIVE)
        for event in events:
            data.append({
                'id': event.id,
                'name': event.name
            })
        return data

    def get(self, request, *args, **kwargs):
        context = {}
        context['events'] = self.get_type_events()
        return self.render_to_response(context)


class RepresentationCharacterDataList(LoginRequiredMixin, PermissionRequiredMixin,
                               JSONResponseMixin, View):

    model = RepresentationDetailModel

    def get_character(self):
        data = []
        characters = RepresentationDetailModel.CHOICE_CHARACTER
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


class RepresentationSaveProcess(View):
    data_line = {}
    data_models = {}

    def format_date(self, date):
        return date

    def save_representation(self, project):
        representation = Representation()
        representation.project = project
        representation.ppi = self.format_date(self.data_line.get('ppi'))
        representation.ppg = self.format_date(self.data_line.get('ppg'))
        representation.type_event = self.data_line.get('type_event')
        representation.save()
        return representation

    def save_detail_model_representation(self, project_line):
        for detail in self.data_models:
            representation_detail_model = RepresentationDetailModel()
            representation_detail_model.representation = project_line

            representation_detail_model.profile = detail.get('profile')
            representation_detail_model.model_id = detail.get('model').get('id')
            representation_detail_model.character = detail.get('character').get('id')
            representation_detail_model.currency = detail.get('currency')
            representation_detail_model.budget = detail.get('budget')
            representation_detail_model.budget_cost = detail.get('budget_cost')
            representation_detail_model.schedule = detail.get('schedule')
            representation_detail_model.save()