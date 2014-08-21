# -*- coding: utf-8 -*-

from datetime import datetime
import os
import json
import urllib2
import logging

from django.conf import settings
from PIL import Image
from django.utils.encoding import smart_str
from django.views.generic import View
from django.db import connections

from django.contrib.contenttypes.models import ContentType
from apps.common.view import LoginRequiredMixin
from apps.common.view import JSONResponseMixin
from apps.fileupload.models import Picture, PictureThumbnail
from apps.fileupload.serialize import serialize
from django.core.files import File
from apps.sp.models.Model import Model, ModelFeatureDetail
from apps.sp.models.Entry import Entry
from apps.sp.models.Country import Country
from apps.sp.models.Currency import Currency
from apps.sp.models.Brand import Brand
from apps.sp.models.Commercial import Commercial, CommercialDateDetail
from apps.sp.models.Client import Client, TypeClient
from apps.sp.models.Project import Project, ProjectDetailDeliveries, ProjectClientDetail
from apps.sp.models.Feature import Feature, FeatureValue
from apps.sp.models.Casting import TypeCasting
from apps.sp.models.Payment import Payment
from apps.sp.models.Extras import Extras, ExtrasDetailModel, ExtraDetailParticipate
from apps.sp.models.Casting import Casting, CastingDetailModel, CastingDetailParticipate
from apps.sp.models.PhotoCasting import PhotoCasting, PhotoCastingDetailModel, \
    PhotoCastingDetailParticipate, TypePhotoCasting
from apps.sp.models.Representation import Representation, RepresentationDetailModel, TypeEvent


class ModelProcessMigrate(LoginRequiredMixin, JSONResponseMixin, View):
    LOGGER = 'migration'
    url_sisadmini_api = "http://192.168.1.3/sistemas/sisadmini/api/data_complete.php"
    url_bco_api = "http://192.168.1.3/sistemas/sisadmini/api/data_bco.php"
    numberdoc = 0

    def set_attributes(self):
        url_base = os.getcwd()
        self.log = logging.getLogger('migration')
        self.url_media = '%s/%s/%s/%s' %(url_base, 'static', 'media', '000000')
        self.relation_commercial_project = []

        self.setTypeDoc()
        self.setConditions()
        self.setStatusModel()
        self.setTypeClients()
        self.setStatusClie()
        self.setGenericComercial()
        self.setExtraCharacter()
        self.setTypeCasting()
        self.setTypeEventRepresentation()
        self.setTypePhotoCasting()
        self.setClientCastingAbroad()
        self.setClientExtraAbroad()

    def json_reader(self, json_file):
        ROOT_PATH = settings.ROOT_PATH
        file_path = ROOT_PATH + '/apps/common/db_data/json/%s.json' %json_file
        file = open(file_path, 'r')
        json_data = json.load(file)
        file.close()
        return json_data

    def setClientCastingAbroad(self):
        self.casting_abroad = ["CL078", "CL079", "CL214", "CL226",
                             "CL228", "CL245", "CL265", "CL267",
                             "CL269", "CL270", "CL271", "CL284",
                             "CL286"]

    def setClientExtraAbroad(self):
        self.extra_abroad = ['CL228']

    def setTypePhotoCasting(self):
        self.type_photo_casting = {
            '1': TypePhotoCasting.objects.get(name='Fotografico'),
            '2': TypePhotoCasting.objects.get(name='Archico Fotografico'),
            '3': TypePhotoCasting.objects.get(name='Archivo Fotografico con Callback')
        }

    def setTypeEventRepresentation(self):
        self.type_event_representation= {
            '1': TypeEvent.objects.get(name='Foto'),
            '2': TypeEvent.objects.get(name='Comercial'),
            '3': TypeEvent.objects.get(name='Evento'),
            '4': TypeEvent.objects.get(name='Reposicion')
        }

    def setGenericComercial(self):
        entry = Entry()
        entry.name = 'Rubro Generico'
        entry.save()
        self.brand = Brand()
        self.brand.entry = entry
        self.brand.name = 'Marca Generica'
        self.brand.save()

    def setExtraCharacter(self):
        self.extra_character = {
            '1': ExtrasDetailModel.CHARACTER_EXTRA,
            '2': ExtrasDetailModel.CHARACTER_SPECIAL_EXTRA
        }

    def setTypeCasting(self):
        self.type_casting = {
            '1': [TypeCasting.objects.get(name='Especifico')],
            '2': [TypeCasting.objects.get(name='Archivo')],
            '3': [TypeCasting.objects.get(name='Archivo'), TypeCasting.objects.get(name='Callback')],
            '4': [TypeCasting.objects.get(name='Especifico'), TypeCasting.objects.get(name='Scouting')],
            '5': [TypeCasting.objects.get(name='Archivo'), TypeCasting.objects.get(name='Scouting')],
            '6': [TypeCasting.objects.get(name='Especifico'), TypeCasting.objects.get(name='Callback')],
            '7': [TypeCasting.objects.get(name='Especifico'), TypeCasting.objects.get(name='Archivo')],
            '8': [TypeCasting.objects.get(name='Especifico'), TypeCasting.objects.get(name='Archivo'), TypeCasting.objects.get(name='Scouting')],
            '9': [TypeCasting.objects.get(name='Especifico'), TypeCasting.objects.get(name='Archivo'), TypeCasting.objects.get(name='Callback')],
            '10': [TypeCasting.objects.get(name='Archivo Fotografico')],
            '11': [TypeCasting.objects.get(name='Casting Fotografico')],
        }

    def delete(self):
        Client.objects.all().delete()
        Entry.objects.all().delete()
        Model.objects.all().delete()
        Project.objects.all().delete()

    def start_migration(self):
        self.delete()
        self.set_attributes()


        self.log.debug('comenzo: ' + datetime.now().strftime('%d/%m/%Y %H:%M'))
        data_model = self.get_list_model()
        data_model = self.get_detail_feature(data_model)
        self.insert_model(data_model)
        self.log.debug('termino: '+ datetime.now().strftime('%d/%m/%Y %H:%M'))
        # self.data_client = self.insert_data_client()

        #Insert Data
        # self.insert_entry_brand_commercial()
        # data_projects = self.insert_project()
        # data_commercial = self.get_data_commercial()

    def insert_model(self, data_model):

        for model in data_model:
            try:
                _model = Model()
                _model.model_code = model.get('model_code')
                _model.type_doc = model.get('type_doc')
                _model.number_doc = model.get('number_doc')
                _model.status = model.get('status')
                _model.name_complete = model.get('name_complete')
                _model.birth = model.get('birth')
                _model.gender = model.get('gender')
                _model.address = model.get('address')
                _model.email = model.get('email')
                _model.nationality = model.get('nationality')
                _model.phone_fixed = model.get('phone_fixed', '').replace('NINGUNA','').replace('NA','')
                _model.phone_mobil = model.get('phone_mobil', '').replace('NINGUNA','').replace('NA','')
                _model.height = model.get('height')
                _model.weight = model.get('weight')
                _model.terms = model.get('terms', False)
                _model.save()
                self.insert_photos(_model, model.get('photos'))
                self.insert_feature_value(_model, model.get('features'))
                print('save model: ' + model.get('model_code') + ' | '+_model.name_complete)
            except Exception,e:
                import pdb;pdb.set_trace()
                self.log.debug(e.message + ' | ' + model.get('model_code'))

    def insert_feature_value(self, model, features):
        for feature in features:
            model_feature_detail = ModelFeatureDetail()
            model_feature_detail.model = model
            model_feature_detail.feature_value = feature.get('feature_value')
            model_feature_detail.description = feature.get('description') if feature.get('description') != 'NINGUNA' else None
            model_feature_detail.save()

    def insert_photos(self, model, photos):
        for photo in photos:
            try:
                slug = photo.split('/')[-1]
                f = open(photo)
                file =  File(f)
                file.name = slug

                picture = Picture()
                picture.content_type = ContentType.objects.get_for_model(model)
                picture.object_id = model.id
                picture.file = file
                picture.save()
                files = [serialize(picture)]
                thumbnails = PictureThumbnail.save_all_thumbnails(picture)
                if thumbnails is not None:
                    for file in files:
                        file.update({'thumbnailUrl': thumbnails.get('file')})
                    self.save_main_image(model, picture)
                else:
                    import pdb;pdb.set_trace()
                    self.log.debug('Foto no registrada'+ ' | '+ photo)
            except Exception, e:
                import pdb;pdb.set_trace()

    def save_main_image(self, model, picture):
        main_image = None
        picture = Picture.objects.filter(
            content_type = picture.content_type,
            object_id =picture.object_id

        ).latest('created')

        thumbnails = picture.get_all_thumbnail()

        for thumbnail in thumbnails:
            if thumbnail.get('type') == 'Small':
                main_image = thumbnail.get('url')

        model.main_image = main_image
        model.save()

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
                client.update({'type': 'b'})
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
        ruc = 0
        for client in client_json:
            status = None

            type = client.get('type', None)
            if type is None:
                #Sisadmini
                if client.get('id') in self.casting_abroad:
                    status = Client.STATUS_ABROAD

            else:
                #Sisbco
                if client.get('id') in self.extra_abroad:
                    status = Client.STATUS_ABROAD


            old_codes = []
            #Ignore client
            if client.get('cod_cliente') in ['CL001']:
                continue
            if client.get('ruc') is None:
                status = Client.STATUS_FAKE

            if client.get('ruc') in rucs:
                index = get_client_by_ruc(clients, client.get('ruc'))
                codes = clients[index].get('old_code')
                codes.append({
                    'cod_cliente':client.get('cod_cliente'),
                    'type': client.get('type', 'm')
                })
                clients[index].update({
                    'old_code': codes
                })
            else:
                old_codes.append({
                    'cod_cliente':client.get('cod_cliente'),
                    'type': client.get('type', 'm')
                })
                temp = {
                    'old_code': old_codes,
                    'ruc': client.get('ruc'),
                    'sis': client.get('sis'),
                    'name': client.get('nombre'),
                    'types': self.types_clie.get(str(client.get('tipo_cli'))),
                    'status': self.status_clie.get(str(client.get('estado'))),
                }
                if status is not None:
                    ruc += 1
                    temp.update({
                        'status':status,
                        'ruc': str(ruc)
                    })
                else:
                    rucs.append(client.get('ruc'))

                clients.append(temp)

        for new_client in clients:
            try:
                client = Client()
                client.ruc = new_client.get('ruc')
                client.name = new_client.get('name')
                client.status = new_client.get('status')
                client.save()
                new_client.update({'client':  client})
                for type in new_client.get('types'):
                    client.type_client.add(type)
                print('add client: ' + client.name)
            except Exception,e :
                import pdb;pdb.set_trace()
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

    def get_repre_budget_cost(self, detail_models):
        cost = 0
        for detail in detail_models:
            cost += float(detail.get('pago'))
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
        castings = self.json_reader('castings')
        extras = projects.get('extras')
        representations = projects.get('representation')
        photos = projects.get('photo')

        self.insert_representation(representations)
        self.insert_photo_casting(photos)
        # self.insert_extras(extras)
        # self.insert_casting(castings)

    def insert_photo_casting(self, photos):
        for photo in photos:
            if photo.get('nom_proyect') is not None:
                start_production = photo.get('fecha_cod')
                if photo.get('inicio') is not None:
                    if photo.get('inicio').split('/')[1] == photo.get('fecha_cod').split('/')[1] and \
                                    photo.get('inicio').split('/')[2] == photo.get('fecha_cod').split('/')[2]:
                        start_production = photo.get('inicio')

                end_productions = photo.get('fecha_final')
                if end_productions is None:
                    end_productions = photo.get('fech_fotos')
                    if end_productions is None or len(end_productions) >10 or len(end_productions) <= 9:
                        end_productions = start_production

                end_productions = end_productions.replace('-', '/')
                if photo.get('cod_ordcsfot') in ['10-12F110', '11-07F020']:
                    end_productions = start_production
                project = Project()
                project.commercial = self.get_commercial(photo.get('cod_ordcsfot'), photo.get('nom_proyect'), photo.get('fech_fotos'))
                project.line_productions = Project.LINE_PHOTO
                project.code = photo.get('cod_ordcsfot')[6:8]
                project.start_productions = self.format_date(start_production)
                project.end_productions = self.format_date(end_productions)
                project.currency = self.get_currency(photo.get('soles'))
                project.budget = photo.get('presupuesto')
                project.budget_cost = 0
                project.observations = photo.get('observaciones')
                if photo.get('last_version') == '0':
                    project.status = self.get_status_project(photo.get('estado'))
                else:
                    if photo.get('last_version') == photo.get('version'):
                        project.version = int(photo.get('version'))
                        project.status = Project.STATUS_FINISH
                    else:
                        project.version = int(photo.get('version'))
                        project.status = Project.STATUS_EXTEND
                project.save()
                project = Project.objects.get(pk=project.id)
                if photo.get('prientrega') is not None:
                    project_detail_delivery = ProjectDetailDeliveries()
                    project_detail_delivery.project = project
                    project_detail_delivery.delivery_date = self.format_date(photo.get('prientrega'))
                    project_detail_delivery.save()

                if project.get_code() == photo.get('cod_ordcsfot'):
                    _photo_casting = PhotoCasting()
                    _photo_casting.project = project
                    _photo_casting.type_casting = self.type_photo_casting.get(str(photo.get('tipo_cast')))
                    _photo_casting.realized = self.format_date(photo.get('realiza'))
                    _photo_casting.save()
                    self.insert_project_client(photo.get('cod_ordcsfot'), project, photo.get('clientes'))
                    data_payment = {
                        'condiciones': [{'name': photo.get('condiciones')}],
                        'fact_a': photo.get('fact_a'),
                        'type': 'b'
                    }
                    self.insert_payment(project, data_payment)
                    self.insert_detail_model_photo()
                    print('add photo casting: ' + photo.get('cod_ordcsfot'))
                else:
                    import pdb;pdb.set_trace()

    def insert_project_client(self, cod, project, details):
        type_project = 'm'
        if project.line_productions in [Project.LINE_PHOTO, Project.LINE_EXTRA, Project.LINE_REPRESENTATION]:
            type_project = 'b'

        for detail in details:
            type_model,type  = self.get_type_client(detail)
            if detail.get(type) != 'CL001' and detail.get(type) is not None:
                try:
                    project_client_detail = ProjectClientDetail()
                    project_client_detail.project = project
                    project_client_detail.type = type_model
                    project_client_detail.client = self.get_client_old_code(detail.get(type), type_project)
                    project_client_detail.save()
                except Exception, e:
                    import pdb;pdb.set_trace()

    def get_client_old_code(self, code, type):
        for client in self.data_client:
            for old_code in client.get('old_code'):
                if code == old_code.get('cod_cliente') and old_code.get('type') == type:
                    return client.get('client')
        import pdb;pdb.set_trace()
        return None

    def get_type_client(self, detail):
        type = None
        key = ''
        if detail.has_key('agencia'):
            type = TypeClient.objects.get(name='Agencia')
            key = 'agencia'
        if detail.has_key('realizadora'):
            type = TypeClient.objects.get(name='Realizadora')
            key = 'realizadora'
        if detail.has_key('productora'):
            type = TypeClient.objects.get(name='Productora')
            key = 'productora'
        return type, key

    def insert_representation(self, representations):
        for representation in representations:
            if representation.get('cod_ordrep') in ['21-05R010']:
                continue
            if representation.get('nom_proyect') is not None:
                start_production = representation.get('fecha_cod')
                if representation.get('inicio') is not None:
                    if representation.get('inicio').split('/')[1] == representation.get('fecha_cod').split('/')[1]:
                        start_production = representation.get('inicio')

                end_productions = representation.get('fecha_final')
                if end_productions is None:
                    end_productions = start_production
                project = Project()
                project.commercial = self.get_commercial(representation.get('cod_ordrep'), representation.get('nom_proyect'), representation.get('f_evento'))
                project.line_productions = Project.LINE_REPRESENTATION
                project.code = representation.get('cod_ordrep')[6:8]
                project.start_productions = self.format_date(start_production)
                project.end_productions = self.format_date(end_productions)
                project.currency = self.get_extra_currency(representation.get('modelos'))
                project.budget = representation.get('presupuesto')
                project.budget_cost = self.get_repre_budget_cost(representation.get('modelos'))
                project.observations = representation.get('obs')
                if representation.get('last_version') == '0':
                    project.status = self.get_status_project(representation.get('estado'))
                else:
                    if representation.get('last_version') == representation.get('version'):
                        project.version = int(representation.get('version'))
                        project.status = Project.STATUS_FINISH
                        self.close_commercial(project.commercial)
                    else:
                        project.version = int(representation.get('version'))
                        project.status = Project.STATUS_EXTEND
                project.save()
                project = Project.objects.get(pk=project.id)
                if project.get_code() == representation.get('cod_ordrep'):
                    _representation = Representation()
                    _representation.project = project
                    _representation.ppg = self.format_date(representation.get('ppg'))
                    _representation.type_event = self.type_event_representation.get(representation.get('evento'))
                    _representation.save()
                    self.insert_project_client(representation.get('cod_ordrep'), project, representation.get('clientes'))
                    self.insert_detail_model_representation(_representation, representation.get('modelos'))

                    data_payment = {
                        'condiciones': [{'name': representation.get('condiciones')}],
                        'fact_a': representation.get('fact_a'),
                        'type': 'b'
                    }
                    self.insert_payment(project, data_payment)
                    print('add representation: ' + representation.get('cod_ordrep'))
                else:
                    import pdb;pdb.set_trace()

    def close_commercial(self, commercial):
        commercial.status = Commercial.STATUS_TERMINATE
        commercial.save()

    def insert_payment(self, project, data):
        try:
            payment = Payment()
            payment.project = project
            payment.conditions = data.get('condiciones')
            if data.get('fact_a') is not None and data.get('fact_a') != 'CL001':
                if len(data.get('fact_a')) == 5 :
                    paymnet_client = self.get_client_old_code(data.get('fact_a'), data.get('type'))
                    if paymnet_client is not None:
                        payment.client = paymnet_client
            payment.save()
        except Exception, e:
            import pdb;pdb.set_trace()

    def insert_detail_model_representation(self, representation, detail_models):

        for detail in detail_models:
            try:
                representation_detail_model = RepresentationDetailModel()
                representation_detail_model.representation = representation
                representation_detail_model.character = detail.get('personaje')
                representation_detail_model.profile = detail.get('caracteristicas')
                representation_detail_model.budget = detail.get('presupuesto')
                representation_detail_model.currency = self.get_currency(detail.get('moneda'))
                representation_detail_model.budget_cost = detail.get('pago')
                representation_detail_model.save()
            except Exception, e:
                import pdb;pdb.set_trace()


    def insert_casting(self, castings):

        for casting in castings:
            if casting.get('nombre') is not None:
                start_production = casting.get('fecha_emision')
                if casting.get('fecha_ini') is not None:
                    if casting.get('fecha_ini').split('/')[1] == casting.get('fecha_emision').split('/')[1]:
                        start_production = casting.get('fecha_ini')

                end_productions = casting.get('fecha_final')
                if end_productions is None:
                    end_productions = casting.get('ppg')
                    if end_productions is None:
                        end_productions = casting.get('p_entrega')
                        if end_productions is None:
                            end_productions = start_production
                project = Project()
                project.commercial = self.get_commercial(casting.get('cod_ordcast'), casting.get('nombre'), casting.get('film_comer'))
                project.line_productions = Project.LINE_CASTING
                project.code = casting.get('cod_ordcast')[6:8]
                project.start_productions = self.format_date(start_production)
                project.end_productions = self.format_date(end_productions)
                project.currency = self.get_currency(casting.get('moneda'))
                project.budget = casting.get('presupuesto')
                project.budget_cost = casting.get('precasting')
                project.observations = casting.get('observaciones')
                if casting.get('last_version') == '0':
                    project.status = self.get_status_project(casting.get('estado'))
                else:
                    if casting.get('last_version') == casting.get('version'):
                        project.version = int(casting.get('version'))
                        project.status = Project.STATUS_FINISH
                    else:
                        project.version = int(casting.get('version'))
                        project.status = Project.STATUS_EXTEND
                project.save()
                project = Project.objects.get(pk=project.id)

                if casting.get('p_entrega') is not None:
                    project_detail_delivery = ProjectDetailDeliveries()
                    project_detail_delivery.project = project
                    project_detail_delivery.delivery_date = self.format_date(casting.get('p_entrega'))
                    project_detail_delivery.save()

                if project.get_code() == casting.get('cod_ordcast'):
                    _casting = Casting()
                    _casting.project = project
                    _casting.ppg = self.format_date(casting.get('ppg'))
                    _casting.realized = self.format_date(casting.get('ini_rea'))
                    _casting.save()
                    if casting.get('tipo_cas') is not None:
                        for type in self.type_casting.get(str(casting.get('tipo_cas'))):
                            _casting.type_casting.add(type)
                    self.insert_project_client(casting.get('cod_ordcast'), project, casting.get('clients'))
                    print('add casting: ' + casting.get('cod_ordcast'))
                else:
                    import pdb;pdb.set_trace()

    def insert_extras(self, extras):
        for extra in extras:
            if extra.get('nom_proyect') is not None:
                start_production = extra.get('fecha_cod')
                if extra.get('inicio') is not None:
                    if extra.get('fecha_cod').split('/')[1] == extra.get('inicio').split('/')[1]:
                        start_production = extra.get('inicio')

                end_productions = extra.get('fecha_final')
                if end_productions is None:
                    end_productions = extra.get('filmacion')
                    if end_productions is None or len(end_productions) >10 or len(end_productions) <= 9:
                        end_productions = start_production
                end_productions = end_productions.replace('-', '/')
                print('add extra: ' + extra.get('cod_ordext'))
                if extra.get('cod_ordext') == '11-06E010':
                    pass
                project = Project()
                project.commercial = self.get_commercial(extra.get('cod_ordext'), extra.get('nom_proyect'), extra.get('filmacion'))
                project.line_productions = Project.LINE_EXTRA
                project.code = extra.get('cod_ordext')[6:8]
                project.start_productions = self.format_date(start_production)
                project.end_productions = self.format_date(end_productions)
                project.currency = self.get_extra_currency(extra.get('modelos'))
                project.budget = extra.get('presupuesto')
                project.budget_cost = self.get_extra_budget_cost(extra.get('modelos'))
                project.observations = extra.get('observaciones')
                project.status = self.get_status_project(extra.get('estado'))
                if extra.get('last_version') == '0':
                    project.status = self.get_status_project(extra.get('estado'))
                else:
                    if extra.get('last_version') == extra.get('version'):
                        project.version = int(extra.get('version'))
                        project.status = Project.STATUS_FINISH
                    else:
                        project.version = int(extra.get('version'))
                        project.status = Project.STATUS_EXTEND
                project.save()
                project = Project.objects.get(pk=project.id)

                _extra = Extras()
                _extra.project = project
                _extra.save()

                if project.get_code() == extra.get('cod_ordext'):
                    self.insert_project_client(extra.get('cod_ordext'), project, extra.get('clientes'))
                    print('add extra: ' + extra.get('cod_ordext'))
                    # self.insert_coordinator(extra.get('coordinadores'), extra)
                    # self.inset_extra_models(extra.get('modelos'), extra)
                else:
                    import pdb;pdb.set_trace()

    def insert_coordinator(self, coordinators, extra):
        pass

    def inset_extra_models(self, models, extra):
        for model in models:
            extra_detail_model = ExtrasDetailModel()
            extra_detail_model.extras = extra
            extra_detail_model.quantity = model.get('cant')
            extra_detail_model.profile = model.get('modelo')
            extra_detail_model.feature = model.get('caracteristicas')
            extra_detail_model.character = self.extra_character.get(model.get('personaje'))
            extra_detail_model.currency = self.get_extra_currency(model.get('moneda'))
            extra_detail_model.budget = model.get('presupuesto')
            extra_detail_model.budget_cost = model.get('pago_real')
            extra_detail_model.schedule = model.get('observaciones')
            extra_detail_model.save()

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
                return feature_value[0]
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
        return "select m.mod_cod, m.cri_cod, c.cri_desc, m.cri_item, m.mc_obs from mod_cri m " \
               "inner join criterios_cabecera c " \
               "on c.cri_cod = m.cri_cod " \
               "where mod_cod='"+model_code+"' " \
               "group by m.mod_cod, m.cri_cod, c.cri_desc, m.cri_item, m.mc_obs"

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
                            'description': row[4],
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

            sql = "select mod_nom ||' '|| mod_ape as name_complete," \
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
                if type_doc is None or document == "NINGUNA":
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
                    'photos': self.get_photos(row[1])
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