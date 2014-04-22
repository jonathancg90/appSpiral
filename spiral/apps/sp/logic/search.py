# -*- coding: utf-8 -*-

import logging
from django.db.models import Q

from apps.sp.models.Model import Model

log = logging.getLogger(__name__)


class Search(object):
    MESSAGE_ERR_GENERIC = 'Ha ocurrido un error en la busqueda'
    MESSAGE_ERR_PARAM = 'Parametro de bsuqueda incorrecto'
    TYPE_BASIC = 1
    TYPE_ADVANCE = 2

    def __init__(self):
        self._type_search = self.TYPE_BASIC
        self._params = {}
        self._message = {}
        self._result = []
        self._order_by = None
        self._camp_result = {
            'model': [],
            'feature': [],
            'photos': [],
            'video': []
        }

    def set_all_camp(self):
        self._camp_result.update({
            'model': ['all'],
            'feature': ['all'],
            'photos': ['all'],
            'video': ['all']
        })

    def set_type(self, type):
        self._type_search = type

    def set_params(self, params):
        self._params = params

    def basic_search(self):
        models = []
        try:
            if 'text' in self._params:
                import pdb;pdb.set_trace()
                models = Model.objects.filter(
                    Q(name__contains=self._params.get('text')) |
                    Q(last_name__contains=self._params.get('text'))
                )
        except ValueError, e:
            self._message.update({'error': self.MESSAGE_ERR_PARAM})
            log.exception(e.message)
        except Exception, e:
            self._message.update({'error': self.MESSAGE_ERR_GENERIC})
            log.exception(e.message)
        return models

    def advance_search(self):
        pass

    def run(self):
        result = []
        try:
            if self._type_search == self.TYPE_BASIC:
                result = self.basic_search()
            if self._type_search == self.TYPE_ADVANCE:
                result = self.advance_search()
            return result
        except Exception, e:
            log.exception(e.message)
        return self._result


