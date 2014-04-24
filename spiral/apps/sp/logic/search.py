# -*- coding: utf-8 -*-

import logging
from django.db import connection

from apps.sp.models.Model import Model, ModelFeatureDetail
from apps.sp.models.Feature import Feature, FeatureValue


log = logging.getLogger(__name__)


class Search(object):
    MESSAGE_ERR_GENERIC = 'Ha ocurrido un error en la busqueda'
    MESSAGE_ERR_PARAM = 'Parametro de bsuqueda incorrecto'
    MESSAGE_ERR_NOT_CONNECTION = 'Not exixts connection'
    MESSAGE_ERR_CURSOR = 'Ocurrio un error al ejecutar la consulta'
    TYPE_BASIC = 1
    TYPE_ADVANCE = 2

    MODE_SENSITIVE = 1 #Exacto
    MODE_INSENSITIVE = 0 #Inexacto

    def __init__(self):
        self._type_search = self.TYPE_BASIC
        self._params = {}
        self._limit = 20
        self._mode = self.MODE_INSENSITIVE
        self._debug = False
        self._message = {}
        self._result = []
        self._table_model_column = {}
        self._sql = ''
        self._args = []
        self._order_by = None
        self._camp_result = {
            'model': [],
            'feature': [],
            'photos': [],
            'video': []
        }

    def set_tables_names(self):
        self._table_model = getattr(Model, '_meta').db_table
        self._table_model_name_complete = self._table_model + "." + getattr(Model, '_meta').get_field('name_complete').column
        self._table_model_status = self._table_model + "." + getattr(Model, '_meta').get_field('status').column
        self._table_model_phone_fixed = self._table_model + "." + getattr(Model, '_meta').get_field('phone_fixed').column
        self._table_model_phone_mobil = self._table_model + "." + getattr(Model, '_meta').get_field('phone_mobil').column

        self._table_model_column['text'] = [
            self._table_model_name_complete,
            self._table_model_phone_fixed,
            self._table_model_phone_mobil
            ]

        self._table_feature = getattr(Feature, '_meta').db_table
        self._table_feature_value = getattr(FeatureValue, '_meta').db_table
        self._table_product_model_feature = getattr(ModelFeatureDetail, '_meta').db_table

    def set_all_camp(self):
        self._camp_result.update({
            'model': ['all'],
            'feature': [],
            'photos': [],
            'video': []
        })

    def set_debug(self, value):
        self._debug = value

    def set_type(self, type):
        self._type_search = type

    def set_params(self, params):
        self._params = params

    def set_mode(self, mode):
        self._mode = mode

    def get_columns(self):
        camps = '*'
        for model_camp in self._camp_result.get('model'):
            if model_camp == 'all':
                return '*'
            else:
                camps = self._table_model+'.'+model_camp
        return camps

    def get_tables(self):
        return self._table_model

    def get_default_filter(self):
        return self._table_model_status + '!=' + str(Model.STATUS_DISAPPROVE) + ' AND ' \
               + self._table_model_status + '!=' + str(Model.STATUS_INACTIVE) + ' AND '

    def set_sql_base(self):
        self._sql = 'SELECT %s FROM %s WHERE %s' % (self.get_columns(), self.get_tables(), self.get_default_filter())
        if self._debug:
            print '============='
            print 'Base query: '+self._sql

    def add_filters(self):
        for param in self._params:
            if param == "text":
                if self.MODE_INSENSITIVE == self._mode:
                    self.search_insensitive(param)
                elif self.MODE_SENSITIVE == self._mode:
                    self.search_sensitive(param)
        if self._debug:
            print '============='
            print 'Filter Query: '+self._sql

    def search_insensitive(self, param):
        columns = self._table_model_column.get(param)
        ind_column = 0
        for column in columns:
            ind_column += 1
            words = self._params.get(param).split(' ')
            ind_word = 0
            for word in words:
                ind_word +=1
                self._args.append('%'+ word +'%')
                self._sql = self._sql + column + " like %s "
                if len(words) > ind_word:
                    self._sql = self._sql + " or "
            if len(columns) > ind_column:
                self._sql = self._sql + " or "

    def search_sensitive(self, param):
        columns = self._table_model_column.get(param)
        ind_column = 0
        for column in columns:
            ind_column +=1
            search = self._params.get(param)
            if self._table_model_name_complete == column:
                words = self._params.get(param).split(' ')
                ind_word = 0
                for word in words:
                    ind_word +=1
                    self._args.append('%'+ word +'%')
                    self._sql = self._sql + column + " like %s "
                    if len(words) > ind_word:
                        self._sql = self._sql + " and "
            else:
                self._args.append('%'+ search +'%')
                self._sql = self._sql + column + " like %s "
            if len(columns) > ind_column:
                self._sql = self._sql + " or "

    def start_cursor(self):
        try:
            self.cursor = connection.cursor()
        except:
            raise SearchException(self.MESSAGE_ERR_NOT_CONNECTION)

    def _get_cursor_result(self):
        items = []
        desc = []
        try:
            self.start_cursor()
            self.cursor.execute(self._sql, self._args)
            desc = self.cursor.description
            items = self.cursor.fetchall()
            if self._debug:
                print '============='
                print 'Filter Execute: '+self._sql + ' Args: ' + self._args
        except Exception, e:
            self._message.update({'error': self.MESSAGE_ERR_CURSOR})
            log.exception(e.message)

        return items, desc

    def basic_search(self):
        models = []
        try:
            if 'text' in self._params:
                self.add_filters()
                items, desc = self._get_cursor_result()
                for row in items:
                    row = dict(zip([col[0] for col in desc], row))
                    models.append(row)

        except ValueError, e:
            self._message.update({'error': self.MESSAGE_ERR_PARAM})
            log.exception(e.message)
        except Exception, e:
            self._message.update({'error': self.MESSAGE_ERR_GENERIC})
            log.exception(e.message)
        return models

    def run(self):
        self.set_tables_names()
        try:
            self.set_sql_base()
            if self._type_search == self.TYPE_BASIC:
                self.result = self.basic_search()
            if self._type_search == self.TYPE_ADVANCE:
                pass
            return self.result
        except Exception, e:
            log.exception(e.message)
        return self._result


class SearchException(Exception):
    pass