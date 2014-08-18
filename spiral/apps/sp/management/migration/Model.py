# -*- coding: utf-8 -*-

from datetime import datetime
import os
import json
import urllib2
import logging

from django.conf import settings
from django.utils.encoding import smart_str
from django.views.generic import View
from django.db import connections

from apps.common.view import LoginRequiredMixin
from apps.common.view import JSONResponseMixin
from apps.sp.models.Model import Model
from apps.sp.models.Entry import Entry
from apps.sp.models.Country import Country
from apps.sp.models.Currency import Currency
from apps.sp.models.Brand import Brand
from apps.sp.models.Commercial import Commercial, CommercialDateDetail
from apps.sp.models.Client import Client, TypeClient
from apps.sp.models.Project import Project
from apps.sp.models.Feature import Feature, FeatureValue


class ModelProcessMigrate(LoginRequiredMixin, JSONResponseMixin, View):
    LOGGER = 'migration'
    url_sisadmini_api = "http://192.168.1.3/sistemas/sisadmini/api/data_complete.php"
    url_bco_api = "http://192.168.1.3/sistemas/sisadmini/api/data_bco.php"
    numberdoc = 0

    def set_attributes(self):
        url_base = os.getcwd()
        self.log = logging.getLogger('migration')
        self.url_media = '%s/%s/%s' %(url_base, 'static', 'media')
        self.relation_commercial_project = []

        self.setTypeDoc()
        self.setConditions()
        self.setStatusModel()
        self.setTypeClients()
        self.setStatusClie()
        self.setGenericComercial()

    def json_reader(self, json_file):
        ROOT_PATH = settings.ROOT_PATH
        file_path = ROOT_PATH + '/apps/common/db_data/json/%s.json' %json_file
        file = open(file_path, 'r')
        json_data = json.load(file)
        file.close()
        return json_data

    def setGenericComercial(self):
        entry = Entry()
        entry.name = 'Rubro Generico'
        entry.save()
        self.brand = Brand()
        self.brand.entry = entry
        self.brand.name = 'Marca Generica'
        self.brand.save()

    def delete(self):
        Client.objects.all().delete()
        Entry.objects.all().delete()
        Project.objects.all().delete()

    def start_migration(self):
        self.delete()
        self.set_attributes()
        self.log.debug('comenzo: ' + datetime.now().strftime('%d/%m/%Y %H:%M'))
        data_model = self.get_list_model()
        data_model = self.get_detail_feature(data_model)
        self.log.debug('termino: '+ datetime.now().strftime('%d/%m/%Y %H:%M'))
        #self.data_client = self.insert_data_client()

        #Insert Data
        #self.insert_entry_brand_commercial()
        #data_projects = self.insert_project()
        # data_commercial = self.get_data_commercial()

    def insert_entry_brand_commercial(self):
        try:
            query = "select id, name, status from sp_entry"
            model_cursor = connections['commercial'].cursor()
            model_cursor.execute(query)
            for row in model_cursor.fetchall():
                entry = Entry()
                entry.name = row[1]
                entry.status = row[2]
                entry.save()
                print('add entry: ' + row[1])
                self.insert_brand_by_entry(row[0], entry)
        except:
            self.log.debug('Fallo entry')

    def insert_brand_by_entry(self, old_entry_id, new_entry):
        try:
            query = "select id, name, status from sp_brand where entry_id='"+str(old_entry_id)+"'"
            brand_cursor = connections['commercial'].cursor()
            brand_cursor.execute(query)
            for row in brand_cursor.fetchall():
                brand = Brand()
                brand.name = row[1]
                brand.status = row[2]
                brand.entry = new_entry
                brand.save()
                print('add brand: ' + row[1])
                self.insert_commercial_by_brand(row[0], brand)
        except:
            self.log.debug('Fallo Brand')

    def insert_commercial_by_brand(self, old_brand_id, new_brand):
        try:
            query = "select c.id, c.name, c.status, p.project_code, c.realized from sp_commercial c inner join sp_project p on p.id=c.project_id where c.brand_id='"+str(old_brand_id)+"'"
            commercial_cursor = connections['commercial'].cursor()
            commercial_cursor.execute(query)
            for row in commercial_cursor.fetchall():
                commercial = Commercial()
                commercial.name = row[1]
                commercial.status = row[2]
                commercial.brand =new_brand
                commercial.save()
                print('add commercial: ' + row[1])
                if row[4] is not None:
                    commercial_date_detail = CommercialDateDetail()
                    commercial_date_detail.commercial = commercial
                    commercial_date_detail.date = row[4]
                    commercial_date_detail.save()
                self.relation_commercial_project.append({
                    'commercial': commercial,
                    'project_code': row[3]
                })
        except:
            self.log.debug('Fallo Commercial')

    def get_clients_json(self):
        try:
            #Miraflores
            url = '%s?type=%s' %(self.url_sisadmini_api, "C")
            result = urllib2.urlopen(url)
            self.sis_client = json.loads(result.read())
            #Barranco
            url = '%s?type=%s' %(self.url_bco_api, "C")
            result = urllib2.urlopen(url)
            self.bco_client = json.loads(result.read())
            #Match
            clients = self.sis_client
            for client in self.bco_client:
                clients.append(client)
            return clients
        except Exception, e:
            return []

    def insert_data_client(self):
        def get_client_by_ruc(data_client, ruc):
            for client in data_client:
                if client.get('ruc') == ruc:
                    return data_client.index(client)

        clients= []
        rucs = []
        client_json = self.get_clients_json()
        for client in client_json:
            #Falta validar clientes sin RUC
            old_codes = []
            if client.get('ruc') in ['CL001'] or client.get('ruc') is None:
               continue
            if client.get('ruc') in rucs:
                index = get_client_by_ruc(clients, client.get('ruc'))
                codes = clients[index].get('old_code')
                codes.append(client.get('cod_cliente'))
                clients[index].update({
                    'old_code': codes
                })
            else:
                rucs.append(client.get('ruc'))
                old_codes.append(client.get('id'))
                clients.append({
                    'old_code': old_codes,
                    'ruc': client.get('ruc'),
                    'sis': client.get('sis'),
                    'name': client.get('nombre'),
                    'types': self.types_clie.get(str(client.get('tipo_cli'))),
                    'status': self.status_clie.get(str(client.get('estado'))),
                })
        for new_client in clients:
            client = Client()
            client.ruc = new_client.get('ruc')
            client.name = new_client.get('name')
            client.status = new_client.get('status')
            client.save()
            for type in new_client.get('types'):
                client.type_client.add(type)
            print('add client: ' + client.name)
        return clients

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

    def get_commercial(self, cod_project, name, filmacion):
        for relation in self.relation_commercial_project:
            if relation.get('project_code') == cod_project:
                return relation.get('commercial')
        commercial = Commercial()
        commercial.name = name
        commercial.brand = self.brand
        commercial.save()
        filmacion = self.format_date(filmacion)
        if filmacion is not None:
            comercial_date_detail = CommercialDateDetail()
            comercial_date_detail.commercial = commercial
            comercial_date_detail.date = filmacion
            comercial_date_detail.save()
        return commercial

    def format_date(self, date):
        try:
            if date is not None:
                date = datetime.strptime(date, "%d/%m/%Y")
                return "%s-%s-%s" % (date.year, date.month, date.day)
            return date
        except:
            return None

    def get_extra_budget_cost(self, detail_models):
        cost = 0
        for detail in detail_models:
            cost += float(detail.get('pago_real'))
        return cost

    def get_currency(self, currency):
        if currency == 'D':
            return Currency.objects.get(symbol='S/.')
        elif currency == 'S':
            return Currency.objects.get(symbol='$')
        return None


    def get_extra_currency(self, details):
        for detail in details:
            if detail.get('moneda') is not None:
                return self.get_currency(detail.get('moneda'))
        return None

    def get_status_project(self, status):
        if str(status) == "1":
            return Project.STATUS_START
        if str(status) == "2":
            return Project.STATUS_STAND_BY
        if str(status) == "3":
            return Project.STATUS_FINISH

    def insert_project(self):
        projects = self.json_reader('projects')
        extras = projects.get('extras')
        for extra in extras:
            if extra.get('nom_proyect') is not None:
                start_production = extra.get('fecha_cod')
                if extra.get('inicio') is not None:
                    if extra.get('fecha_cod').split('/')[1] == extra.get('inicio').split('/')[1]:
                        start_production = extra.get('inicio')

                end_productions = extra.get('fecha_final')
                if end_productions is None:
                    end_productions = extra.get('filmacion')

                project = Project()
                project.commercial = self.get_commercial(extra, extra.get('nom_proyect'), extra.get('filmacion'))
                project.line_productions = Project.LINE_EXTRA
                project.start_productions = self.format_date(start_production)
                project.end_productions = self.format_date(end_productions)
                project.currency = self.get_extra_currency(extra.get('modelos'))
                project.budget = extra.get('presupuesto')
                project.budget_cost = self.get_extra_budget_cost(extra.get('modelos'))
                project.observations = extra.get('observaciones')
                project.status = self.get_status_project(extra.get('estado'))
                project.save()
                project = Project.objects.get(pk=project.id)
                import pdb;pdb.set_trace()
                if project.get_code() == extra.get('cod_ordext'):
                    self.insert_coordinator(extra.get('coordinadores'))
                    self.inset_extra_models(extra.get('modelos'))
                    self.insert_client(extra.get('clientes'))
                else:
                    import pdb;pdb.set_trace()


        photos = projects.get('photo')
        representations = projects.get('representation')
        import pdb;pdb.set_trace()

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
        if feature_name == 'DISTRITO' and value != 'CHOSICA':
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
        if value == 'LOCUTOR DE RADIO, TV':
            return 'Locutor'

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
                    original = str(feature_name) + ' - ' + str(value_name)
                    change = str(_feature_name) + ' - ' + str(_value_name)
                    self.log.debug('feature_value multiple o nulo: '+str(feature_value)+ ' | ' + original + ' | ' + change)
        except Exception, e:
            original = str(feature_name) + ' - ' + str(value_name)
            self.log.debug(e.message + ' | ' + original)
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
                        if value[0] in ['EXCLUSIVO', 'ACEPTO', 'WEB']:
                            model.update({
                                'terms':  True
                            })
                        if value[0] == 'RECHAZO':
                            model.update({
                                'terms':  False
                            })
                    if row[2] == 'LUGAR NACIMIENTO':
                        try:
                            country = Country.objects.get(name=value[0])
                            model.update({
                                'nationality': country
                            })
                        except:
                            self.log.debug('pais no encontrado ' + value[0])

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
                  "from modelos order by mod_cod"

            # limit 1000 offset 0
            # Limit:  cantidad a mostrar
            #Offset: a partir de que posicion
            model_cursor = connections['model'].cursor()
            model_cursor.execute(sql)
            for row in model_cursor.fetchall():
                type_doc= self.get_type_doc(row[2])
                document = row[3]
                if type_doc is None:
                    type_doc = Model.TYPE_FAKE
                    self.numberdoc += 1
                    document = str(self.numberdoc)
                data_models = {
                    'name_complete': row[0],
                    'model_code': row[1],
                    'type_doc': type_doc,
                    'number_doc': document,
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
            self.log.debug(e.message + ': get_list_model')
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
