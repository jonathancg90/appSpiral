# -*- coding: utf-8 -*-

from django.views.generic import View
from django.db import connections

from apps.common.view import LoginRequiredMixin
from apps.common.view import JSONResponseMixin
from apps.sp.models.Model import Model


class ModelProcessMigrate(LoginRequiredMixin, JSONResponseMixin, View):

    def set_attributes(self):
        self.setTypeDoc()

    def start_migration(self):
        self.set_attributes()
        data_model = self.get_list_model()
        import pdb;pdb.set_trace()

    def setTypeDoc(self):
        self.type_doc = [
            {
                'id_old': '01',
                'id_new': Model.TYPE_DNI
            },
            {
                'id_old': '03',
                'id_new': Model.TYPE_CARNET
            },
            {
                'id_old': '02',
                'id_new': Model.TYPE_PASSPORT
            },
            {
                'id_old': '05',
                'id_new': Model.TYPE_DNI
            }
        ]

    def setConditions(self):
        self.conditions = [
            {
                'id_old': 1,
                'id_new': True
            },
            {
                'id_old': 2,
                'id_new': False
            },
            {
                'id_old': 3,
                'id_new': True
            },
            {
                'id_old': 4,
                'id_new': True
            }
        ]

    def set_status_model(self):
        self.status_mod = [
            {
                'id_old': 1,
                'id_new': Model.STATUS_ACTIVE
            },
            {
                'id_old': 2,
                'id_new': Model.STATUS_ACTIVE
            },
            {
                'id_old': 3,
                'id_new': Model.STATUS_INACTIVE
            },
            {
                'id_old': 4,
                'id_new': Model.STATUS_INACTIVE
            }
        ]

    def convert_date_birth(self, date):
        return date

    def get_list_model(self):
        data = []
        try:
            cursor = connections['model'].cursor()
            sql = "select mod_nom || mod_ape as name_complete," \
                  "mod_cod as model_code, " \
                  "td_cod as type_doc, " \
                  "mod_dni as number_doc, " \
                  "cod_est as status, " \
                  "mod_fec_nac as birth, " \
                  "mod_dir as address, " \
                  "mod_email as email, " \
                  "mod_tel as phone_fixed, " \
                  "mod_cel as phone_mobil, " \
                  "mod_estatura as height, " \
                  "mod_peso as weight " \
                  "from modelos"

            cursor.execute(sql)
            for row in cursor.fetchall():
                data_models = {
                    'name_complete': row[0],
                    'model_code': row[1],
                    'type_doc': row[2],
                    'number_doc': row[3],
                    'status': row[4],
                    'birth': self.convert_date_birth(row[5]),
                    'address': row[6],
                    'email': row[7],
                    'phone_fixed': row[8],
                    'phone_mobil': row[9],
                    'height': row[10],
                    'weight': row[11]
                }
                data.append(data_models)
            return data
        except Exception, e:
            import pdb;pdb.set_trace()
            return data

    def insert_model(self, data):
        model = Model()
        model.name_complete = data.get('name_complete')
        model.model_code = data.get('model_code')
        model.type_doc = data.get('type_doc')
        model.number_doc = data.get('number_doc')
        model.status = data.get('status')
        model.birth = data.get('birth')
        model.gender = data.get('gender')
        model.address = data.get('address')
        model.email = data.get('email')
        model.nationality = data.get('nationality')
        model.city = data.get('city')
        model.phone_fixed = data.get('phone_fixed')
        model.phone_mobil = data.get('phone_mobil')
        model.height = data.get('height')
        model.weight = data.get('weight')
        model.terms = data.get('terms')
