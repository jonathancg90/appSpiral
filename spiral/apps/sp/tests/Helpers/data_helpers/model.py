# -*- encoding: utf-8 -*-
from apps.sp.management.commands_helpers.insert import InsertHelperMixin
from apps.sp.models.Model import Model, ModelFeatureDetail
from apps.sp.models.Country import Country
from apps.sp.models.Feature import FeatureValue


class ModelHelper(InsertHelperMixin):
    entity = Model

    def set_data(self):
        self.objects_to_insert = [
            {
                "model_code": "000023",
                "type_doc": Model.TYPE_DNI,
                "number_doc": "46411023",
                "status": Model.STATUS_ACTIVE,
                "name_complete": "Jonathan Percy Perez",
                "birth": "1990-08-12",
                "gender": Model.GENDER_MASC,
                "address": "Jr. Catalino Miranda 354",
                "email": "jonathancgfere@gmail.com",
                "nationality": Country.objects.latest('created'),
                "phone_fixed": "4774571",
                "phone_mobil": "96372612756",
                "height": 1.65,
                "weight": 40,
                "last_visit": "2014-08-12",
            },
            {
                "model_code": "000001",
                "type_doc": Model.TYPE_DNI,
                "number_doc": "46443023",
                "status": Model.STATUS_ACTIVE,
                "name_complete": "Jonathan",
                "birth": "1990-08-12",
                "gender": Model.GENDER_MASC,
                "address": "Jr. Catalino Miranda 356",
                "email": "jonathancg90@gmail.com",
                "nationality": Country.objects.latest('created'),
                "phone_fixed": "4771071",
                "phone_mobil": "96372678756",
                "height": 1.60,
                "weight": 56,
                "last_visit": "2013-08-12",
            },
            {
                "model_code": "000002",
                "type_doc": Model.TYPE_DNI,
                "number_doc": "46443223",
                "status": Model.STATUS_WEBSITE,
                "name_complete": "Rosa",
                "birth": "1987-12-08",
                "gender": Model.GENDER_FEM,
                "address": "Jr. Catalino Soledad 356",
                "email": "rosamadelaine@gmail.com",
                "nationality": Country.objects.latest('created'),
                "phone_fixed": "4772371",
                "phone_mobil": "96372543756",
                "height": 1.67,
                "weight": 79,
                "last_visit": "2013-09-12",
            },
            {
                "model_code": "000003",
                "type_doc": Model.TYPE_DNI,
                "number_doc": "46443213",
                "status": Model.STATUS_WEBSITE,
                "name_complete": "Rosaura de la cruz",
                "birth": "1987-01-01",
                "gender": Model.GENDER_FEM,
                "address": "Jr. Catalino Soledad 356",
                "email": "rosaura1232@gmail.com",
                "nationality": Country.objects.latest('created'),
                "phone_fixed": "4772371",
                "phone_mobil": "96372513756",
                "height": 1.67,
                "weight": 79,
                "last_visit": "2014-01-04",
            },
        ]


class ModelFeatureHelper(InsertHelperMixin):
    entity = ModelFeatureDetail

    def set_data(self):
        self.objects_to_insert = [
            {
                "model": Model.objects.get(pk=1),
                "feature_value": FeatureValue.objects.get(pk=1),
                "description": None,
            },
            {
                "model": Model.objects.get(pk=1),
                "feature_value": FeatureValue.objects.get(pk=2),
                "description": None,
            },
            {
                "model": Model.objects.get(pk=2),
                "feature_value": FeatureValue.objects.get(pk=3),
                "description": None,
            },
            {
                "model": Model.objects.get(pk=2),
                "feature_value": FeatureValue.objects.get(pk=4),
                "description": None,
            },
            {
                "model": Model.objects.get(pk=3),
                "feature_value": FeatureValue.objects.get(pk=5),
                "description": None,
            }
        ]