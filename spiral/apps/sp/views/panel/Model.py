# -*- coding: utf-8 -*-

import json
from datetime import date

from django.conf import settings
from django.db import transaction
from django.core.files.storage import default_storage
from django.views.generic import View, TemplateView, CreateView
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from apps.fileupload.models import Picture, PictureThumbnail
from apps.fileupload.serialize import serialize
from apps.fileupload.response import JSONResponse, response_mimetype

from apps.sp.models.Model import Model, ModelFeatureDetail
from apps.sp.models.Feature import Feature, FeatureValue
from apps.sp.models.Pauta import DetailPauta
from apps.common.view import JSONResponseMixin
from apps.common.view import LoginRequiredMixin, PermissionRequiredMixin


class ModelControlTemplateView(LoginRequiredMixin, PermissionRequiredMixin,
                               TemplateView):
    template_name = 'panel/model/profile.html'
    model = Model

    def get_context_data(self, **kwargs):
        context = super(ModelControlTemplateView, self).get_context_data(**kwargs)
        context['doc_types'] = json.dumps(Model.get_types())
        context['genders'] = json.dumps(Model.get_genders())
        context['menu'] = 'model'
        context['features'] = json.dumps(Feature.get_data_features())
        code = self.request.GET.get('pk')
        if code is not None:
            id = Model.objects.get(model_code=code).id
            context['pk'] = code
            context['id'] = id
        return context


class ModelDataJsonView(LoginRequiredMixin, PermissionRequiredMixin,
                        JSONResponseMixin, View):
    model = Model
    MESSAGE_SUCCESSFUL = 'El modelo encontrado'
    MESSAGE_ERR_NOT_FOUND = 'El modelo no ha sido encontrado'
    MESSAGE_ERR = 'Ocurrio un error al buscar al modelo'

    def get_model_profile(self, model):
        web = True if model.status == Model.STATUS_WEBSITE is None else False
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
            "phone_fixed": model.phone_fixed,
            "phone_mobil": model.phone_mobil,
            "pauta": self.get_pauta(model),
            "height": str(model.height),
            "weight": str(model.weight),
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

    def get_pauta(self, model):
        detail_pauta = DetailPauta.objects.filter(model=model)
        detail_pauta= detail_pauta.count()
        return detail_pauta

    def parse_data(self, model):

        if model.last_visit is not None:
            model.last_visit = model.last_visit.strftime("%d/%m/%Y")
        else:
            model.last_visit = 'Aún no ha sido citado'

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
        ).order_by('-taken_date')
        for picture in pictures:
            data.append({
                'main_id': picture.id,
                'show': True,
                'main_picture': picture.file.name,
                'thumbs': picture.get_all_thumbnail(),
                'taken': picture.taken_date.strftime("%d/%m/%Y") if picture.taken_date is not None else 'Sin fecha',
                'features': []
            })
        return data



    def get_model_commercial(self, model):
        data = []
        commercial = model.model_has_commercial_set.all()
        commercial = commercial.select_related('commercial', 'commercial__project')
        for com in commercial:
            data.append({
                'name': com.commercial.name,
                'code': com.commercial.project,
                'realized': com.commercial.realized,
                'contact': ''
            })
        return data

    def get(self ,request, *args, **kwargs):
        model_code = kwargs.get('pk')
        try:
            model = Model.objects.select_related('country',
                                                 'model_has_commercial_set',
                                                 'model_feature_detail_set'
            ).get(model_code=model_code)
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
        except Model.DoesNotExist, e:
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


class ModelCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                      JSONResponseMixin, View):
    SAVE_SUCCESSFUL = 'Modelo registrado'
    ERROR_MODEL_DNI = "Numero de DNI duplicado"
    ERROR_MODEL_SAVE = 'ocurrio un error al tratar de grabar la informacion del modelo'
    permissions = {
        "permission": ('sp.add_model', ),
    }

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(ModelCreateView, self).dispatch(request, *args, **kwargs)

    def get_model(self):
        model = Model()
        model.model_code = Model.get_code()
        return model

    def save_model(self, data):
        if self.kwargs.get('pk', None) is None:
            if Model.objects.filter(number_doc=data.get('num_doc')).exists():
                return None, self.ERROR_MODEL_DNI
        else:
            if Model.objects.filter(number_doc=data.get('num_doc')).\
                    exclude(model_code=self.kwargs.get('pk', None)).exists():
                return None, self.ERROR_MODEL_DNI
        try:
            model = self.get_model()
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
            context['id'] = model.id
        return self.render_to_response(context)


class ModelUpdateView(ModelCreateView):
    SAVE_SUCCESSFUL = 'Modelo actualizado'
    ERROR_MODEL_DNI = "Numero de DNI duplicado"
    ERROR_MODEL_SAVE = 'ocurrio un error al tratar de grabar la informacion del modelo'
    permissions = {
        "permission": ('sp.change_model', ),
    }

    def get_model(self):
        return Model.objects.get(model_code=self.kwargs.get('pk'))


class PictureModelCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                             CreateView):
    model = Picture
    thumb_options = PictureThumbnail.THUMBS
    permissions = {
        "permission": ('fileupload.add_picture', ),
    }


    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(PictureModelCreateView, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class):
        form = super(PictureModelCreateView, self).get_form(form_class)
        form.fields['object_id'].required = False
        form.fields['content_type'].required = False
        form.fields['taken_date'].required = False
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


class ModelFeatureUpdateView(LoginRequiredMixin, PermissionRequiredMixin,
                             JSONResponseMixin, View):
    UPDATE_SUCCESSFUL = 'Datos descriptivos grabados'
    ERROR_MODEL_SAVE = 'ocurrio un error al tratar de grabar la informacion del modelo'
    permissions = {
        "permission": ('sp.change_modelfeaturedetail', ),
    }

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


class DeleteImageModelView(LoginRequiredMixin, PermissionRequiredMixin,
                           JSONResponseMixin, View):
    entity_class = Model
    STATUS_ERROR = 'warning'
    MESSAGE_SUCCESS = 'Foto eliminada'
    MESSAGE_ERROR = 'No se ha podido eliminar su foto'
    permissions = {
        "permission": ('sp.delete_picture', ),
    }

    def delete_thumbnails(self, picture):
        thumbnails = PictureThumbnail.objects.filter(picture=picture)
        for thumbnail in thumbnails:
            url = '%s/%s' %(settings.MEDIA_ROOT, thumbnail.file)
            default_storage.delete(url)
            thumbnail.delete()

    def get(self, request, *args, **kwargs):
        context = {}
        picture_id = kwargs.get('pk')
        picture = Picture.objects.get(id=picture_id)
        url_file = '%s/%s' %(settings.MEDIA_ROOT, picture.file.name)
        if default_storage.exists(url_file):
            default_storage.delete(url_file)
            self.delete_thumbnails(picture)
            picture.delete()
            context['message'] = self.MESSAGE_SUCCESS
        else:
            context['message'] = self.MESSAGE_ERROR
            context['status'] = self.STATUS_ERROR

        return self.render_json_response(context)


class QuickModelUpdateView(LoginRequiredMixin, PermissionRequiredMixin,
                           JSONResponseMixin, View):
    model = Model
    STATUS_ERROR = 'warning'
    MESSAGE_SUCCESS = 'Modelo actualizado'
    MESSAGE_ERROR = 'No se ha podido actualizar'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(QuickModelUpdateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context = {}
        try:
            data = json.loads(request.body)
            model = Model.objects.get(model_code=data.get('model_code'))
            model.phone_fixed = data.get('phone_fixed')
            model.weight = data.get('weight')
            model.height = data.get('height')
            model.address = data.get('address')
            model.email = data.get('email')
            model.phone_mobil = data.get('phone_mobil')
            model.save()
            context['message'] = self.MESSAGE_SUCCESS
        except Exception , e:
            context['message'] = self.MESSAGE_ERROR
            context['status'] = self.STATUS_ERROR

        return self.render_to_response(context)


class ModelFeatureCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                             JSONResponseMixin, View):
    SAVE_SUCCESSFUL = 'Datos descriptivos grabados'
    ERROR_MODEL_SAVE = 'La carracteristica ya existe registrada'
    permissions = {
        "permission": ('sp.add_modelfeaturedetail', ),
    }

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


class ModelFeatureDeleteView(LoginRequiredMixin, PermissionRequiredMixin,
                             JSONResponseMixin, View):
    DELETE_SUCCESSFUL = 'Carracteristica eliminada'
    ERROR_MODEL_FEATURE_DELETE = 'ocurrio un error al tratar de eliminar la informacion del modelo'
    permissions = {
        "permission": ('sp.delete_modelfeaturedetail', ),
    }

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


class ModelSimpleSearchView(LoginRequiredMixin, PermissionRequiredMixin,
                            JSONResponseMixin, View):
    MESSAGE_SUCCESS = 'Modelo encontrado'
    ERROR_SEARCH = 'Ha ocurrido un error al momento de buscar al modelo'
    WARNING_NOT_FOUND = 'No se ha encontrado ningun modelo con ese nombre'
    model = Model

    def search_model(self, data):
        try:
            result = []
            models = Model.objects.filter(name_complete__contains=data.get('name'))
            for model in models:
                result.append({
                    'id': model.id,
                    'name': model.name_complete,
                    'document': '%s %s' %(model.get_type_doc_display(), model.number_doc)
                })
            return result
        except:
            return None

    def post(self, request, *args, **kwargs):
        context = {}
        data = json.loads(request.body)
        result = self.search_model(data)
        if result is None:
            context["status"] = "error"
            context["message"] = self.ERROR_SEARCH
        elif len(result) == 0:
            context["status"] = "warning"
            context["message"] = self.WARNING_NOT_FOUND
        else:
            context["status"] = "success"
            context["message"] = self.MESSAGE_SUCCESS
            context["models"] = result
        return self.render_to_response(context)