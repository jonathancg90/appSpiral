# -*- coding: utf-8 -*-
import json
from django.conf import settings
from apps.sp.models.Feature import Feature, FeatureValue
from apps.sp.models.Country import Country
from apps.sp.models.City import City
from apps.sp.models.Currency import Currency
from apps.sp.models.Client import TypeClient
from apps.sp.models.Casting import TypeCasting
from apps.sp.models.Representation import TypeEvent
from apps.sp.models.PhotoCasting import TypePhotoCasting
from apps.sp.models.Client import Client
from apps.sp.models.Brand import Brand
from apps.sp.models.Entry import Entry
from apps.sp.models.Commercial import Commercial


class ReaderJsonHelper(object):

    def json_reader(self, json_file):
        ROOT_PATH = settings.ROOT_PATH
        file_path = ROOT_PATH + '/apps/common/db_data/json/%s.json' %json_file
        file = open(file_path, 'r')
        json_data = json.load(file)
        file.close()
        return json_data


class ReaderTxtHelper(object):

    def data_parse(self, file):
        txt = '/apps/common/db_data/%s.txt' %file

        ROOT_PATH = settings.ROOT_PATH
        file_path = ROOT_PATH + txt

        file = open(file_path, 'r')
        line = True

        while line:
            line = file.readline().strip()

            if len(line) < 1 or line[0] == '#':
                continue

            yield [e.strip() for e in line.split('\t')]


class FeatureHelper(ReaderJsonHelper):

    def insert_data(self):
        features = self.json_reader('features')
        self.insert_features(features)

    def insert_features(self, features):
        for feature in features:
            _feature = Feature()
            _feature.name = feature.get('name')
            _feature.type = feature.get('type')
            _feature.save()
            for value in feature.get('values'):
                _feature_value = FeatureValue()
                _feature_value.feature = _feature
                _feature_value.name = value.get('name')
                _feature_value.save()


class CountryHelper(ReaderJsonHelper):

    def insert_data(self):
        countries = self.json_reader('countries')
        self.insert_countries(countries)

    def insert_countries(self, countries):
        for country in countries:
            _country = Country()
            _country.name = country.get('name')
            _country.nationality = country.get('nationality')
            _country.save()
            for city in country.get('cities'):
                _city = City()
                _city.name = city.get('name')
                _city.country = _country
                _city.save()


class TypeClientHelper(object):

    def insert_data(self):
        names = ['Productora', 'Realizadora', 'Agencia']
        for name in names:
            type_client = TypeClient()
            type_client.name = name
            type_client.save()


class TypeCastingHelper(object):

    def insert_data(self):
        names = ['Especifico', 'Archivo',
                 'Scouting', 'Callback',
                 'Archivo Fotografico',
                 'Casting Fotografico']
        for name in names:
            type_casting = TypeCasting()
            type_casting.name = name
            type_casting.save()


class TypeEventHelper(object):

    def insert_data(self):
        names = ['Foto', 'Comercial',
                 'Evento', 'Reposicion']
        for name in names:
            type_event = TypeEvent()
            type_event.name = name
            type_event.save()


class TypePhotoCastingHelper(object):

    def insert_data(self):
        names = ['Archico Fotografico', 'Archivo Fotografico con Callback']
        for name in names:
            type_photo_casting = TypePhotoCasting()
            type_photo_casting.name = name
            type_photo_casting.save()


class CurrencyHelper(object):

    def insert_data(self):
        coins = [
            {
                'name': 'Soles',
                'symbol':  'S/.'
            },
            {
                'name': 'Dolares Americanos',
                'symbol':  '$'
            }
        ]
        for coin in coins:
            currency = Currency()
            currency.name = coin.get('name')
            currency.symbol = coin.get('symbol')
            currency.save()


class DataTestHelper(object):

    def insert_client(self):
        if not Client.objects.filter(name='Productor').exists():
            client_productor = Client()
            client_productor.name = 'Productor'
            client_productor.ruc = '12345678901'
            client_productor.save()
            client_productor.type_client.add(TypeClient.objects.get(name= 'Productora'))

        if not Client.objects.filter(name='Realizadora').exists():
            client_director = Client()
            client_director.name = 'Realizadora'
            client_director.ruc = '12333678901'
            client_director.save()
            client_director.type_client.add(TypeClient.objects.get(name='Realizadora'))

        if not Client.objects.filter(name='Agencia').exists():
            client_agency = Client()
            client_agency.name = 'Agencia'
            client_agency.ruc = '12555678901'
            client_agency.save()
            client_agency.type_client.add(TypeClient.objects.get(name= 'Agencia'))

    def insert_commercial(self):
        if not Commercial.objects.filter(name='Comercial de prueba').exists():
            entry = Entry()
            entry.name = 'Rubro de prueba'
            entry.save()

            brand = Brand()
            brand.entry = entry
            brand.name = 'Marca de prueba'
            brand.save()

            commercial = Commercial()
            commercial.brand = brand
            commercial.name = 'Comercial de prueba'
            commercial.save()

    def insert_data(self):
        self.insert_client()
        self.insert_commercial()