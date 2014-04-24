# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from PIL import Image
from StringIO import StringIO
from celery.task import PeriodicTask
from urlparse import urlparse
from datetime import timedelta

from apps.sp.models.Model import Model
from apps.fileupload.models import Picture, PictureThumbnail
from apps.sp.models.Country import Country

import urllib2
import requests
import json


class TabFacebookTask(PeriodicTask):
    run_every = timedelta(minutes=1)
    url = 'http://127.0.0.1:8000/panel/model/model-control/data/'

    def get_country(self, nationality):
        try:
            country = Country.objects.get(nationality=nationality)
            return country
        except ObjectDoesNotExist:
            return None

    def type_document(self, doc_type):
        types = Model.get_types()
        for type in types:
            if type.get('name') == doc_type:
                return type.get('id')
        return None

    def save_image(self, image_url, model):
        picture = Picture()
        picture.content_type = ContentType.objects.get_for_model(model)
        picture.object_id = model.id
        picture.file = self.get_image_url(image_url)
        picture.save()
        PictureThumbnail.save_all_thumbnails(picture)

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

    def save_model(self, data):
        for model_data in data:
            model = Model()
            model.name = model_data.get('name') + ' ' + model_data.get('last_name')
            model.model_code = Model.get_code()
            model.type_doc = self.type_document(model_data.get('type_doc'))
            model.number_doc = model_data.get('num_doc')
            model.address = model_data.get('address')
            model.email = model_data.get('email')
            model.birth = model_data.get('birth')
            model.nationality = self.get_country(model_data.get('nationality'))
            model.save()
            self.save_image(model_data.get('image'), model)

    def get_data(self):
        try:
            result = urllib2.urlopen(self.url)
            return json.loads(result.read())
        except Exception,e:
            return []

    def run(self, **kwargs):
        data = self.get_data()
        self.save_model(data)

