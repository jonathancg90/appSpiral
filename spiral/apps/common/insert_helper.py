# -*- coding: utf-8 -*-
import json
from django.conf import settings
from apps.sp.models.Feature import Feature, FeatureValue
from apps.sp.models.Country import Country
from apps.sp.models.City import City



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

