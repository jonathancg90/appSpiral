# -*- coding: utf-8 -*-

import json

from datetime import date
from django.db import transaction
from django.views.generic import View, TemplateView, CreateView
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from apps.fileupload.models import Picture, PictureThumbnail
from apps.fileupload.serialize import serialize
from apps.fileupload.response import JSONResponse, response_mimetype

from apps.sp.models.Model import Model, ModelFeatureDetail
from apps.sp.models.Feature import Feature, FeatureValue
from apps.common.view import JSONResponseMixin
from apps.common.view import LoginRequiredMixin


class ModelControlTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'panel/model/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ModelControlTemplateView, self).get_context_data(**kwargs)
        context['doc_types'] = json.dumps(Model.get_types())
        context['genders'] = json.dumps(Model.get_genders())
        context['features'] = json.dumps(Feature.get_data_features())
        if self.request.GET.get('pk') is not None:
            context['pk'] = self.request.GET.get('pk')
        return context


class ModelDataJsonView(LoginRequiredMixin, JSONResponseMixin, View):
    MESSAGE_SUCCESSFUL = 'El modelo encontrado'
    MESSAGE_ERR_NOT_FOUND = 'El modelo no ha sido encontrado'
    MESSAGE_ERR = 'Ocurrio un error al buscar al modelo'

    def get_model_profile(self, model):
        web = True if model.last_visit is None else False
        self.parse_data(model)
        data = {
            "id": model.id,
            "code": model.model_code,
            "name_complete": model.name_complete,
            "type_doc": model.get_type_doc_display(),
            "num_doc": model.number_doc,
            "address": model.address,
            "gender": model.gender,
            "email": model.email,
            "main_image": model.main_image,
            "web": web,
            "country": '' if model.city is None else model.city.country.id,
            "city_id": '' if model.city is None else model.city.id,
            "city_name": '' if model.city is None else model.city.name,
            "age": date.today().year - model.birth.year,
            "birth": model.birth.strftime("%d/%m/%Y"),
            "last_visit": model.last_visit,
            "phones": '%s | %s ' %(str(model.phone_mobil), str(model.phone_fixed)),
            "measures": '%s %s | %s %s' %(str(model.weight), 'Kg',  str(model.height), 'mts')
        }
        if model.nationality is None:
            data.update({
                "nationality": 'No ingresado',
            })
        else:
            data.update({
                "nationality": model.nationality.nationality,
                "nationality_id": model.nationality.id,
                })
        return data

    def parse_data(self, model):

        if model.last_visit is not None:
            model.last_visit = model.last_visit.strftime("%d/%m/%Y")
        else:
            model.last_visit = 'Ahun no ha sido citado'

        if model.weight is None:
            model.weight = 0

        if model.height is None:
            model.height = 0

    def get_model_features(self, model):
        data = []
        features = model.model_feature_detail_set.all()
        features = features.select_related('feature_value')
        for feature_detail in features:
            value = feature_detail.feature_value
            data.append({
                'feature_id': value.feature.id,
                'feature': value.feature.name,
                'description': feature_detail.description,
                'value_id': value.id,
                'value': value.name,
                'updated': feature_detail.modified.strftime("%d/%m/%Y"),
                "type": value.feature.get_type_display(),
                "model_feature": feature_detail.id
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
                'show': True,
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
        try:
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
                "message": self.MESSAGE_SUCCESSFUL,
                "status": "success"
            }
        except Model.DoesNotExist:
            data = {
                "status": "warning",
                "message": self.MESSAGE_ERR_NOT_FOUND
            }
        except Exception, e:
            data = {
                "status": "error",
                "message": self.MESSAGE_ERR
            }
        return self.render_to_response(data)


class ModelCreateView(LoginRequiredMixin, JSONResponseMixin, View):
    SAVE_SUCCESSFUL = 'Modelo registrado'
    ERROR_MODEL_DNI = "Numero de DNI duplicado"
    ERROR_MODEL_SAVE = 'ocurrio un error al tratar de grabar la informacion del modelo'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(ModelCreateView, self).dispatch(request, *args, **kwargs)

    def get_model(self):
        return Model()

    def save_model(self, data):
        if self.kwargs.get('pk', None) is None:
            if Model.objects.filter(number_doc=data.get('num_doc')).exists():
                return None, self.ERROR_MODEL_DNI
        else:
            if Model.objects.filter(number_doc=data.get('num_doc')).\
                    exclude(pk=self.kwargs.get('pk', None)).exists():
                return None, self.ERROR_MODEL_DNI
        try:
            model = self.get_model()
            model.model_code = Model.get_code()
            model.name_complete = data.get('name_complete')
            model.type_doc = data.get('type_doc').get('id')
            model.number_doc = data.get('num_doc')
            model.address = data.get('address')
            model.email = data.get('email')
            model.city_id = data.get('city')
            model.phone_fixed = data.get('phone_fixed')
            model.phone_mobil = data.get('phone_mobil')
            model.birth = data.get('birth')
            model.gender = data.get('gender')
            model.weight = data.get('weight', None)
            model.height = data.get('height', None)
            model.nationality_id = data.get('nationality')
            model.save()
            return model, self.SAVE_SUCCESSFUL
        except Exception, e:
            return None, self.ERROR_MODEL_SAVE

    def post(self, request, *args, **kwargs):
        context = {}
        data = json.loads(request.body)
        model, msg = self.save_model(data)
        context['status'] = 'success'
        context['message'] = msg
        if model is None:
            context['status'] = 'warning'
        else:
            context['code'] = model.model_code
        return self.render_to_response(context)


class ModelUpdateView(ModelCreateView):
    SAVE_SUCCESSFUL = 'Modelo actualizado'
    ERROR_MODEL_DNI = "Numero de DNI duplicado"
    ERROR_MODEL_SAVE = 'ocurrio un error al tratar de grabar la informacion del modelo'

    def get_model(self):
        return Model.objects.get(pk=self.kwargs.get('pk'))


class PictureModelCreateView(LoginRequiredMixin, CreateView):
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
        model = Model.objects.get(pk=self.request.POST.get('flag'))
        self.object = form.save(commit=False)
        self.object.content_type = ContentType.objects.get_for_model(model)
        self.object.object_id = model.id
        self.object.save()
        files = [serialize(self.object)]
        thumbnails = self.after_form_valid()
        if thumbnails is not None:
            for file in files:
                file.update({'thumbnailUrl': thumbnails.get('file')})
            self.save_main_image(model)
        else:
            #No se grabo los thumbs
            pass
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def after_form_valid(self):
        return PictureThumbnail.save_all_thumbnails(self.object)

    def save_main_image(self, model):
        main_image = None
        picture = Picture.objects.filter(
            content_type = self.object.content_type,
            object_id =self.object.object_id

        ).latest('created')

        thumbnails = picture.get_all_thumbnail()

        for thumbnail in thumbnails:
            if thumbnail.get('type') == 'Small':
                main_image = thumbnail.get('url')

        model.main_image = main_image
        model.save()

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')


class ModelFeatureUpdateView(LoginRequiredMixin, JSONResponseMixin, View):
    UPDATE_SUCCESSFUL = 'Datos descriptivos grabados'
    ERROR_MODEL_SAVE = 'ocurrio un error al tratar de grabar la informacion del modelo'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(ModelFeatureUpdateView, self).dispatch(request, *args, **kwargs)

    def update_feature_model(self, data):
        model = Model.objects.get(pk=self.kwargs.get('pk'))
        description = data.get('description', None)
        feature_value = data.get('feature')

        model_feature_detail = ModelFeatureDetail.objects.get(pk=data.get('model_feature_id'))
        model_feature_detail.feature_value = FeatureValue.objects.get(pk=feature_value.get('value_id'))
        model_feature_detail.model = model
        model_feature_detail.description = description
        model_feature_detail.save()

        return self.result_json(model_feature_detail)

    def result_json(self, model_feature_detail):
        return {
            "feature_id": model_feature_detail.feature_value.feature.id,
            "feature": model_feature_detail.feature_value.feature.name,
            "value_id": model_feature_detail.feature_value.id,
            "value": model_feature_detail.feature_value.name,
            "description": model_feature_detail.description,
            "updated": model_feature_detail.modified.strftime("%d/%m/%Y"),
            "type": model_feature_detail.feature_value.feature.get_type_display(),
            "model_feature": model_feature_detail.id
        }

    @transaction.commit_manually
    def post(self, request, *args, **kwargs):
        context = {}
        data = json.loads(request.body)
        context['status'] = 'success'
        context['message'] = self.UPDATE_SUCCESSFUL
        try:
            result = self.update_feature_model(data)
            if result is None:
                transaction.rollback()
                context['status'] = 'error'
                context['message'] = self.ERROR_MODEL_SAVE
            else:
                transaction.commit()
                context['feature'] = result
        except Exception, e:
            context['status'] = 'error'
            context['message'] = self.ERROR_MODEL_SAVE
            transaction.rollback()

        return self.render_to_response(context)


class ModelFeatureCreateView(LoginRequiredMixin, JSONResponseMixin, View):
    SAVE_SUCCESSFUL = 'Datos descriptivos grabados'
    ERROR_MODEL_SAVE = 'La carracteristica ya existe registrada'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(ModelFeatureCreateView, self).dispatch(request, *args, **kwargs)

    def save_feature_model(self, data):
        feature_value = data.get('feature_value')

        feature_value = FeatureValue.objects.get(pk=feature_value.get('value_id'))
        feature = feature_value.feature
        model = Model.objects.get(pk=self.kwargs.get('pk'))
        description = data.get('description', None)

        if model.model_feature_detail_set.filter(feature_value__feature=feature).exists():
            if feature.type == Feature.TYPE_UNIQUE:
                return None
            elif feature.type == Feature.TYPE_MULTIPLE:
                if model.model_feature_detail_set.filter(feature_value=feature_value).exists():
                    return None


        model_feature_detail = ModelFeatureDetail()
        model_feature_detail.feature_value = feature_value
        model_feature_detail.model = model
        model_feature_detail.description = description
        model_feature_detail.save()

        return self.result_json(model_feature_detail)

    def result_json(self, model_feature_detail):
        return {
            "feature_id": model_feature_detail.feature_value.feature.id,
            "feature": model_feature_detail.feature_value.feature.name,
            "value_id": model_feature_detail.feature_value.id,
            "value": model_feature_detail.feature_value.name,
            "description": model_feature_detail.description,
            "updated": model_feature_detail.modified.strftime("%d/%m/%Y"),
            "type": model_feature_detail.feature_value.feature.get_type_display(),
            "model_feature": model_feature_detail.id
        }

    @transaction.commit_manually
    def post(self, request, *args, **kwargs):
        context = {}
        data = json.loads(request.body)
        context['status'] = 'success'
        context['message'] = self.SAVE_SUCCESSFUL
        try:
            result = self.save_feature_model(data)
            if result is None:
                transaction.rollback()
                context['status'] = 'warning'
                context['message'] = self.ERROR_MODEL_SAVE
            else:
                transaction.commit()
                context['feature'] = result
        except Exception, e:
            context['status'] = 'error'
            context['message'] = self.ERROR_MODEL_SAVE
            transaction.rollback()

        return self.render_to_response(context)


class ModelFeatureDeleteView(LoginRequiredMixin, JSONResponseMixin, View):
    DELETE_SUCCESSFUL = 'Carracteristica eliminada'
    ERROR_MODEL_FEATURE_DELETE = 'ocurrio un error al tratar de eliminar la informacion del modelo'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(ModelFeatureDeleteView, self).dispatch(request, *args, **kwargs)

    def delete_feature_mode(self, id):
        try:
            model_feature_detail = ModelFeatureDetail.objects.get(pk=id)
            model_feature_detail.delete()
            return True
        except:
            return False

    def post(self, request, *args, **kwargs):
        context = {}
        feature_model_id = json.loads(request.body)
        result = self.delete_feature_mode(feature_model_id)
        context["status"] = "error"
        context["message"] = self.ERROR_MODEL_FEATURE_DELETE
        if result:
            context["status"] = "success"
            context["message"] = self.DELETE_SUCCESSFUL
        return self.render_to_response(context)

