# -*- coding: utf-8 -*-
import urllib
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from PIL import Image
from StringIO import StringIO
from celery.task import PeriodicTask
from urlparse import urlparse
from datetime import timedelta

from apps.sp.models.Model import Model
from apps.sp.models.Model import ModelFeatureDetail
from apps.sp.models.Feature import Feature, FeatureValue
from apps.fileupload.models import Picture, PictureThumbnail
from apps.sp.models.Country import Country
from apps.sp.models.City import City

import urllib2
import requests
import json


class TabFacebookTask(PeriodicTask):
    run_every = timedelta(minutes=1)
    feature = {}
    token = "asdh23498hsdjkn9u32iojrkfns"
    url_get_model = "http://www.spiral.com.pe/facebook/api.php?op=1&token="
    url_update_model = "http://www.spiral.com.pe/facebook/api.php?op=2&token="
    url_photo = "http://spiral.com.pe/casting_big/"

    def get_country(self, nationality):
        try:
            country = Country.objects.get(nationality=nationality)
            return country
        except ObjectDoesNotExist:
            return None

    def get_gender(self, sex):
        if sex == "F":
            return Model.GENDER_FEM
        else:
            return Model.GENDER_MASC

    def get_city(self, city):
        try:
            city = City.objects.get(name=city)
            return city
        except ObjectDoesNotExist:
            return None

    def type_document(self, doc_type):
        types = Model.get_types()
        doc_type = doc_type.upper()
        for type in types:
            if type.get('name').upper() == doc_type:
                return type.get('id')
        return types[1].get('id')

    def save_image(self, image_url, model):
        try:
            picture = Picture()
            picture.content_type = ContentType.objects.get_for_model(model)
            picture.object_id = model.id
            image_url = self.url_photo+image_url
            picture.file = self.get_image_url(image_url)
            picture.save()
            PictureThumbnail.save_all_thumbnails(picture)
        except Exception, e:
            pass

    def get_image_url(self, image_url):
        name = urlparse(image_url).path.split('/')[-1]
        response = requests.get(image_url, stream=True)
        if response.status_code != requests.codes.ok:
            return None
        image = Image.open(StringIO(response.content))
        img_io = StringIO()
        image.save(img_io, format='JPEG')
        img_file = InMemoryUploadedFile(img_io, None, name, 'image/jpeg', img_io.len, None)
        return img_file

    def set_feature(self):
        self.feature['cam_blu'] = Feature.objects.get(name='Talla de ropa')
        self.feature['pant'] = Feature.objects.get(name='Talla de pantalon')
        self.feature['shoes'] = Feature.objects.get(name='Talla de zapatos')
        self.feature['ocu_datos'] = Feature.objects.get(name='Ocupacion')
        self.feature['fb_datos'] = Feature.objects.get(name='Redes sociales')
        self.feature['yt_datos'] = Feature.objects.get(name='Redes sociales')
        self.feature['hobbie'] = Feature.objects.get(name='Hobbies')
        self.feature['color_ojos'] = Feature.objects.get(name='Color de ojos')
        self.feature['larg_cab'] = Feature.objects.get(name='Tamaño de cabello')
        self.feature['tip_cab'] = Feature.objects.get(name='Tipo de cabello')

    @transaction.commit_manually
    def save_model(self, data):
        ids = ''
        for model_data in data:
            try:
                model = Model()
                model.name_complete = model_data.get('nom_datos') + ' ' + model_data.get('app_datos') + ' ' + model_data.get('apm_datos')
                model.model_code = Model.get_code()
                model.type_doc = self.type_document(model_data.get('tipdoc_datos'))
                model.number_doc = model_data.get('num_doc_datos')
                model.address = model_data.get('dir_datos')
                model.email = model_data.get('mail_datos')
                model.birth = model_data.get('fec_datos')
                model.gender = self.get_gender(model_data.get('sexo'))
                model.city = self.get_city(model_data.get('dep_datos'))
                model.nationality = self.get_country(model_data.get('naci_datos'))
                model.phone_fixed = model_data.get('fijo_datos')
                model.phone_mobil = model_data.get('movil_datos')
                model.height = model_data.get('estatura')
                model.terms = model_data.get('terminos')
                model.save()
                ids = ids + model_data.get('id_adulto') + ','
                self.save_model_feature(model, model_data)
                self.save_model_photo(model, model_data)
                self.update_main_image(model)
                transaction.commit()
            except:
                transaction.rollback()
        return ids

    def update_main_image(self, model):
        main_image = None
        picture = Picture.objects.filter(
            content_type=ContentType.objects.get_for_model(model),
            object_id=model.id

        ).latest('created')

        thumbnails = picture.get_all_thumbnail()

        for thumbnail in thumbnails:
            if thumbnail.get('type') == 'Small':
                main_image = thumbnail.get('url')

        model.main_image = main_image
        model.save()

    def save_model_photo(self, model, data):
        if data.get('fot1') != '':
            self.save_image(data.get('fot1'), model)
        if data.get('fot2') != '':
            self.save_image(data.get('fot2'), model)

    def save_model_feature(self, model, data):
        for feature in self.feature:
            try:
                model_feature_detail = ModelFeatureDetail()
                if self.feature[feature] == Feature.objects.get(name='Redes sociales'):
                    if data.get(feature).find('facebook') > 0:
                        feature_value = FeatureValue.objects.get(name='Facebook', feature=self.feature[feature])
                        model_feature_detail.description = data.get(feature)
                        model_feature_detail.feature_value = feature_value
                    if data.get(feature).find('youtube') > 0:
                        feature_value = FeatureValue.objects.get(name='Youtube', feature=self.feature[feature])
                        model_feature_detail.description = data.get(feature)
                        model_feature_detail.feature_value = feature_value
                else:
                    feature_value = FeatureValue.objects.get(name=data.get(feature), feature=self.feature[feature])
                    model_feature_detail.description = None
                    model_feature_detail.feature_value = feature_value

                model_feature_detail.model = model
                model_feature_detail.save()
            except Exception, e:
                pass

    def get_data(self):
        try:
            url = '%s%s' %(self.url_get_model, self.token)
            result = urllib2.urlopen(url)
            return json.loads(result.read())
        except Exception, e:
            return []

    def update_status(self, ids):
        url = '%s%s' %(self.url_update_model, self.token)
        data = urllib.urlencode({"ids":ids})
        result = urllib.urlopen(url, data)
        return json.loads(result.read())

    def parse_data(self, data):
        for model_data in data:
            terms = False
            if len(model_data.get('estatura')) == 0 \
                    or float(model_data.get('estatura').replace(',','.')) > 3:
                estatura = 0
                model_data.update({
                    'estatura': estatura
                })

            if model_data.get('terminos') == 'aceptar':
                terms = True
            model_data.update({
                'terminos': terms
            })
        return data

    def run(self, **kwargs):
        self.set_feature()
        data = self.get_data()
        data = self.parse_data(data)
        ids = self.save_model(data)
        status = self.update_status(ids)
        return status

