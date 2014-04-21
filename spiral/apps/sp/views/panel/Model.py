# -*- coding: utf-8 -*-

import json
from django.db import transaction
from django.views.generic import View, TemplateView, CreateView
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from apps.fileupload.models import Picture, PictureThumbnail
from apps.fileupload.serialize import serialize
from apps.fileupload.response import JSONResponse, response_mimetype

from apps.sp.models.Model import Model, ModelFeatureDetail
from apps.sp.models.Country import Country
from apps.sp.models.Feature import Feature, FeatureValue
from apps.common.view import JSONResponseMixin
from apps.common.view import LoginRequiredMixin


class ModelControlListView(LoginRequiredMixin, TemplateView):
    template_name = 'panel/model/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ModelControlListView, self).get_context_data(**kwargs)
        context['doc_types'] = json.dumps(Model.get_types())
        context['features'] = json.dumps(Feature.get_data_features())
        return context


class ModelDataJsonView(LoginRequiredMixin, JSONResponseMixin, View):

    def get_model_profile(self, model):
        data = {
            "name": model.name,
            "last_name": model.last_name,
            "type_doc": model.get_type_doc_display(),
            "num_doc": model.number_doc,
            "address": model.address,
            "email": model.email,
            "birth": str(model.birth),
            "nationality": model.nationality.nationality,
        }
        return data

    def get_model_features(self, model):
        data = []
        features = model.model_feature_detail_set.all()
        features = features.select_related('feature_value')
        for feature_detail in features:
            value = feature_detail.feature_value
            data.append({
                'feature_id': value.feature.id,
                'feature': value.feature.name,
                'value_id': value.id,
                'value': value.name
            })
        return data

    def get_model_images(self, model):
        data = []
        content_type = ContentType.objects.get_for_model(model)
        pictures = Picture.objects.filter(
            object_id=model.id,
            content_type=content_type
        )
        for picture in pictures:
            data.append({
                'main_id': picture.id,
                'main_picture': picture.file.name,
                'thumbs': picture.get_all_thumbnail()
            })
        return data

    def get_model_commercial(self, model):
        data = []
        commercial = model.model_has_commercial_set.all()
        commercial = commercial.select_related('commercial', 'commercial__project')
        for com in commercial:
            data.append({
                'name': com.commercial.name,
                'code': com.commercial.project.project_code
            })
        return data

    def get(self ,request, *args, **kwargs):
        model_id = kwargs.get('pk')
        model = Model.objects.select_related('country',
                                             'model_has_commercial_set',
                                             'model_feature_detail_set'
        ).get(pk=model_id)
        profile = self.get_model_profile(model)
        features = self.get_model_features(model)
        commercial = self.get_model_commercial(model)
        images = self.get_model_images(model)

        data = {
            "profile": profile,
            "features": features,
            "commercial": commercial,
            "images": images,
        }
        return self.render_to_response(data)


class ModelCreateView(LoginRequiredMixin, JSONResponseMixin, View):
    SAVE_SUCCESSFUL = 'Modelo registrado'
    ERROR_MODEL_SAVE = 'ocurrio un error al tratar de grabar la informacion del modelo'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(ModelCreateView, self).dispatch(request, *args, **kwargs)

    def save_model(self, data):
        try:
            model = Model()
            model.name = data.get('name')
            model.last_name = data.get('last_name')
            model.type_doc = data.get('type_doc').get('id')
            model.number_doc = data.get('num_doc')
            model.address = data.get('address')
            model.email = data.get('email')
            model.birth = data.get('birth')
            model.nationality = Country.objects.get(pk=data.get('nationality').get('id'))
            model.save()
            return model
        except Exception, e:
            return None

    def post(self, request, *args, **kwargs):
        context = {}
        data = json.loads(request.body)
        model = self.save_model(data)

        context['message'] = self.SAVE_SUCCESSFUL
        if model is None:
            context['message'] = self.ERROR_MODEL_SAVE
        context['status'] = 200
        return self.render_to_response(context)


class PictureModelCreateView(CreateView):
    model = Picture
    thumb_options = PictureThumbnail.THUMBS

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(PictureModelCreateView, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class):
        form = super(PictureModelCreateView, self).get_form(form_class)
        form.fields['object_id'].required = False
        form.fields['content_type'].required = False
        return form

    def form_valid(self, form):
        model = Model.objects.get(pk=7)
        self.object = form.save(commit=False)
        self.object.content_type = ContentType.objects.get_for_model(model)
        self.object.object_id = model.id
        self.object.save()
        files = [serialize(self.object)]
        thumbnails = self.after_form_valid()
        if thumbnails is not None:
            for file in files:
                file.update({'thumbnailUrl': thumbnails.get('file')})
        else:
            #No se grabo los thumbs
            pass
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def after_form_valid(self):
        return PictureThumbnail.save_all_thumbnails(self.object)

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')


class ModelFeatureCreateView(LoginRequiredMixin, JSONResponseMixin, View):
    SAVE_SUCCESSFUL = 'Datos descriptivos grabados'
    ERROR_MODEL_SAVE = 'ocurrio un error al tratar de grabar la informacion del modelo'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(ModelFeatureCreateView, self).dispatch(request, *args, **kwargs)

    def save_feature_mode(self, data):
        feature_value = FeatureValue.objects.get(pk=data.get('value_id'))
        feature = feature_value.feature
        model = Model.objects.get(pk=self.kwargs.get('pk'))

        if model.model_feature_detail_set.filter(feature_value__feature=feature).exists():
            if feature.type == Feature.TYPE_UNIQUE:
                detail = model.model_feature_detail_set.get(feature_value__feature=feature)
                detail.feature_value = feature_value
                detail.save()
                return detail
            return None

        model_feature_detail = ModelFeatureDetail()
        model_feature_detail.feature_value = feature_value
        model_feature_detail.model = model
        model_feature_detail.save()

        return model_feature_detail

    @transaction.commit_manually
    def post(self, request, *args, **kwargs):
        context = {}
        feature = json.loads(request.body)
        context['message'] = self.SAVE_SUCCESSFUL
        try:
            result = self.save_feature_mode(feature)
            if result is None:
                transaction.rollback()
                context['message'] = self.ERROR_MODEL_SAVE
            else:
                transaction.commit()
        except Exception, e:
            context['message'] = self.ERROR_MODEL_SAVE
            transaction.rollback()

        context['status'] = 200
        return self.render_to_response(context)


class ModelDataView(LoginRequiredMixin, JSONResponseMixin, View):

    def get(self ,request, *args, **kwargs):
        data = []
        data.append({
            "name":"jonathan",
            "last_name":"Carrasco",
            "type_doc":"DNI",
            "num_doc":"46443224",
            "address":"av. catalino miranda 356 Barranco",
            "email":"jonathancg90@gmail.com",
            "birth":"1990-08-12",
            "nationality":"Peruana",
            "image":"http://spiral.com.pe/facebook/slide/imgs/1.jpg"
        })
        return self.render_to_response(data)