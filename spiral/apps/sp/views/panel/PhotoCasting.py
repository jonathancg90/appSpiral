# -*- coding: utf-8 -*-
from django.views.generic import View

from apps.common.view import LoginRequiredMixin, PermissionRequiredMixin
from apps.common.view import JSONResponseMixin
from apps.sp.models.PhotoCasting import TypePhotoCasting, PhotoCasting,\
    PhotoCastingDetailModel


class TypePhotoCastingDataList(LoginRequiredMixin, PermissionRequiredMixin,
                               JSONResponseMixin, View):

    model = TypePhotoCasting

    def get_types(self):
        data = []
        types = TypePhotoCasting.objects.filter(status=TypePhotoCasting.STATUS_ACTIVE)
        for type in types:
            data.append({
                'id': type.id,
                'name': type.name
            })
        return data

    def get(self, request, *args, **kwargs):
        context = {}
        context['types'] = self.get_types()
        return self.render_to_response(context)


class PhotoCastingSaveProcess(View):
    data_line = {}
    data_models = {}

    def format_date(self, date):
        return date

    def save_photo(self, project):
        photo_casting = PhotoCasting()
        photo_casting.project = project
        photo_casting.use_photo = self.data_line.get('photo_use')
        photo_casting.type_casting = self.data_line.get('type_casting')
        photo_casting.save()
        return photo_casting

    def save_detail_model_photo(self, project_line):
        for detail in self.data_models:
            photo_casting_detail_model = PhotoCastingDetailModel()
            photo_casting_detail_model.photo_casting = project_line
            photo_casting_detail_model.quantity = detail.get('quantity')
            photo_casting_detail_model.profile = detail.get('profile')
            photo_casting_detail_model.feature = detail.get('feature')
            photo_casting_detail_model.character = detail.get('character').get('id')
            photo_casting_detail_model.currency = detail.get('currency')
            photo_casting_detail_model.budget = detail.get('budget')
            photo_casting_detail_model.observations = detail.get('observations')
            photo_casting_detail_model.save()