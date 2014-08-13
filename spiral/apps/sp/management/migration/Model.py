# -*- coding: utf-8 -*-

from datetime import datetime
import os
import json
import urllib2

from django.utils.encoding import smart_str, smart_unicode
from django.views.generic import View
from django.db import connections

from apps.common.view import LoginRequiredMixin
from apps.common.view import JSONResponseMixin
from apps.sp.models.Model import Model
from apps.sp.models.Country import Country
from apps.sp.models.Client import Client, TypeClient
from apps.sp.models.Feature import Feature, FeatureValue


class ModelProcessMigrate(LoginRequiredMixin, JSONResponseMixin, View):
    url_sisadmini_api = "http://192.168.1.3/sistemas/sisadmini/api/data_complete.php"
    url_bco_api = "http://192.168.1.3/sistemas/sisadmini/api/data_bco.php"

    def set_attributes(self):
        url_base = os.getcwd()
        self.url_media = '%s/%s/%s' %(url_base, 'static', 'media')

        self.setTypeDoc()
        self.setConditions()
        self.setStatusModel()
        self.setTypeClients()
        self.setStatusClie()

    def start_migration(self):
        self.set_attributes()
        data_model = self.get_list_model()
        data_model = self.get_detail_feature(data_model)
        import pdb;pdb.set_trace()
        data_client = self.get_data_client()
        data_projects = self.get_data_project()
        data_commercial = self.get_data_commercial()

        self.insert_client(data_client)

    def get_clients_json(self):
        try:
            #Miraflores
            url = '%s?type=%s' %(self.url_sisadmini_api, "C")
            result = urllib2.urlopen(url)
            sis_client = json.loads(result.read())
            #Barranco
            url = '%s?type=%s' %(self.url_bco_api, "C")
            result = urllib2.urlopen(url)
            bco_client = json.loads(result.read())
            #Match
            clients = sis_client
            for client in bco_client:
                clients.append(client)
            return clients
        except Exception, e:
            return []

    def get_project_json(self):
        data = {}
        #Miraflores
        url = '%s?type=%s' %(self.url_sisadmini_api, "M")
        result = urllib2.urlopen(url)
        data_sis = json.loads(result.read())
        #Barranco
        url = '%s?type=%s' %(self.url_bco_api, "B")
        result = urllib2.urlopen(url)
        data_bco = json.loads(result.read())
        data.update({
            'casting':data_sis,
            'extras': data_bco.get('extras'),
            'photo': data_bco.get('photo'),
            'representation': data_bco.get('representation')
        })
        return data

    def get_data_client(self):
        def get_client_by_ruc(data_client, ruc):
            for client in data_client:
                if client.get('ruc') == ruc:
                    return data_client.index(client)

        data= []
        rucs = []
        client_json = self.get_clients_json()
        for client in client_json:
            #Falta validar clientes sin RUC
            old_codes = []
            if client.get('ruc') in rucs:
                index = get_client_by_ruc(data, client.get('ruc'))
                codes = data[index].get('old_code')
                codes.append(client.get('cod_cliente'))
                data[index].update({
                    'old_code': codes
                })
            else:
                rucs.append(client.get('ruc'))
                old_codes.append(client.get('id'))
                data.append({
                    'old_code': old_codes,
                    'ruc': client.get('ruc'),
                    'name': client.get('nombre'),
                    'types': self.types_clie.get(str(client.get('tipo_cli'))),
                    'status': self.status_clie.get(str(client.get('estado'))),
                })
        return data

    def setTypeClients(self):
        productor = TypeClient.objects.get(name='Productora')
        agency = TypeClient.objects.get(name='Agencia')
        director = TypeClient.objects.get(name='Realizadora')

        self.types_clie = {
            '1': [director],
            '2': [productor],
            '3': [agency],
            '4': [],
            '5': [director, productor],
            '6': [director, agency],
            '7': [productor, agency]
        }

    def setStatusClie(self):
        self.status_clie = {
            '1': Client.STATUS_ACTIVE,
            '2': Client.STATUS_INACTIVE
        }


    def get_data_project(self):
        projects = self.get_project_json()

    def insert_client(self, clients):
        for _client in clients:
            client = Client()
            client.name = _client.get('name')
            client.ruc = _client.get('ruc')
            client.address = _client.get('address')
            client.save()
            for type in _client.get('types'):
                client.type_client.add(type)

    def parse_data_feature_value(self, feature_name, value):
        if feature_name == 'DISTRITO':
            return value[:-3]
        if feature_name == 'ANFITRIONAJE':
            return 'Anfitriona'
        if feature_name in ['TALLA - CAMISA', 'TALLA - BLUSA']:
            if value == '2':
                return 'XXS'
            if value == '4':
                return 'XXS'
            if value == '6':
                return 'XS'
            if value == '16':
                return 'L'
            if value == '8':
                return 'S'
            if value == '10':
                return 'S'
            if value == '12':
                return 'M'
            if value == '14':
                return 'M'
            if value == '18':
                return 'L'
            if value == '15 1/2':
                return 'M'

        if value in ['MARRONES', 'PARDOS']:
            return 'Marron'
        if value == 'NEGROS':
            return 'Negro'
        if value in ['ANFITRIONAJE', 'FOTOGRAFICO', 'PASARELA', 'CORREOGRAFIAS (BAILES)', 'COMERCIALES']:
            return 'Modelaje'
        if value == 'VERDES':
            return 'verde'
        if value == 'AZULES':
            return 'Azul'
        if value == 'ADMINISTRACION':
            return 'Administrador'
        if value == 'COREOGRAFIAS (BAILES)':
            return 'Bailar'
        if value in ['CRESPO', 'RIZO']:
            return 'Rizado'

        return value

    def parse_data_feature_name(self, feature_name):
        feature_name = smart_str(feature_name)

        if feature_name == 'TALLA - CAMISA':
            return "Talla de ropa"

        if feature_name == 'CABELLO - COLOR':
            return 'Color de cabello'

        if feature_name == 'TALLA - PANTALON':
            return 'Talla de pantalon'

        if feature_name == 'MODELAJE':
            return 'Hobbies'

        if feature_name == 'TALLA - BLUSA':
            return 'Talla de ropa'

        if feature_name == 'CABELLO - TAMA\xc3\x91O':
            return 'Tamaño de cabello'

        if feature_name == 'CABELLO - TIPO':
            return 'Tipo de cabello'

        if feature_name == 'PAGINAS WEB':
            return 'Redes sociales'

        if feature_name in ['ANFITRIONAJE', 'PROFESION']:
            return 'Ocupacion'
        return feature_name

    def get_feature_value(self, feature_name, value_name):
        ignore = ['GENERO', 'CONDICIONES',  'LUGAR NACIMIENTO',
                  'PROCEDENCIA', 'CASTING 01', 'CASTING 02',
                  'CASTING 03', 'ROPA', 'MES Y A\xc3\x91O', 'COMERCIALES REALIZADOS']
        if smart_str(feature_name) in ignore:
            return None
        try:
            _value_name = self.parse_data_feature_value(feature_name, value_name)
            _feature_name = self.parse_data_feature_name(feature_name)

            feature = Feature.objects.get(name=_feature_name)
            feature_value = FeatureValue.objects.filter(
                feature=feature,
                name=_value_name
            )
            if len(feature_value) == 1:
                return feature_value[0].id
            else:
                ignore_values = ['HI5', 'OTROS', 'OTROS SITIOS WEB']
                if value_name in ignore_values:
                    pass
                else:
                    import pdb;pdb.set_trace()
        except Exception, e:
            import pdb;pdb.set_trace()
        return None

    def get_query_feature_detail(self, model_code):
        return "select m.mod_cod, m.cri_cod, c.cri_desc, m.cri_item, d.cd_desc, m.mc_obs from mod_cri m " \
               "inner join criterios_cabecera c " \
               "on c.cri_cod = m.cri_cod " \
               "inner join criterios_detalles d " \
               "on d.cri_item=m.cri_item " \
               "where mod_cod='"+model_code+"' " \
               "group by m.mod_cod, m.cri_cod, c.cri_desc, m.cri_item, d.cd_desc, m.mc_obs"

    def get_detail_feature(self, data_model):
        for model in data_model:
            gender = None
            query = self.get_query_feature_detail(model.get('model_code'))
            model_cursor = connections['model'].cursor()
            model_cursor.execute(query)
            for row in model_cursor.fetchall():
                query_value = "select cd_desc from criterios_detalles where cri_cod='"+str(row[1])+ "' and cri_item='" + str(row[3]) + "'"
                feature_value_cursor = connections['model'].cursor()
                feature_value_cursor.execute(query_value)
                for value in feature_value_cursor.fetchall():
                    feature_value = self.get_feature_value(row[2], value[0])
                    if feature_value is not None:
                        model.get('features').append({
                            'description': row[5],
                            'feature_value': feature_value
                        })

                    if row[2] == 'GENERO':
                        if value[0] == 'M':
                            model.update({
                                'gender': Model.GENDER_MASC
                            })
                        else:
                            model.update({
                                'gender': Model.GENDER_FEM
                            })
                    if row[2] == 'CONDICIONES':
                        if value[0] == 'EXCLUSIVO':
                            model.update({
                                'terms':  True
                            })
                        else:
                            import pdb;pdb.set_trace()
                    if row[2] == 'LUGAR NACIMIENTO':
                        try:
                            country = Country.objects.get(name=value[0])
                            model.update({
                                'nationality': country
                            })
                        except:
                            import pdb;pdb.set_trace()

            print('add detail: ' + model.get('model_code'))


        return data_model

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

    def setStatusModel(self):
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
        year = date[0:4]
        month = date[4:6]
        day = date[6:8]
        return "%s-%s-%s" % (year, month, day)

    def get_status(self, status_model):
        for status in self.status_mod:
            if status_model == status.get('id_old'):
                return status.get('id_new')
        return Model.STATUS_ACTIVE

    def get_type_doc(self, doc_model):
        for doc in self.type_doc:
            if doc.get('id_old') == doc_model:
                return doc.get('id_new')
        return None

    def get_list_model(self):
        data = []
        try:
            # 00 -> Documento sin especificar
            # 04 -> Libreta militar

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
                  "from modelos where td_cod != '00' and td_cod != '04' "
            model_cursor = connections['model'].cursor()
            model_cursor.execute(sql)
            for row in model_cursor.fetchall():
                data_models = {
                    'name_complete': row[0],
                    'model_code': row[1],
                    'type_doc': self.get_type_doc(row[2]),
                    'number_doc': row[3],
                    'status': self.get_status(row[4]),
                    'birth': self.convert_date_birth(row[5]),
                    'address': row[6],
                    'email': row[7],
                    'phone_fixed': row[8],
                    'phone_mobil': row[9],
                    'height': row[10],
                    'weight': row[11],
                    'features': [],
                    'photos': self.get_photos(row[0])
                }
                print('add: ' + row[1])
                data.append(data_models)
            return data
        except Exception, e:
            import pdb;pdb.set_trace()
            return data

    def get_photos(self, model_code):
        photos = []
        try:
            url = '%s/%s' %(self.url_media, model_code)
            os.chdir(url)
            for file in os.listdir("."):
                photos.append(url + '/' + file)
            return photos
        except:
            return photos

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
