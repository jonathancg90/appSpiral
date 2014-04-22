# -*- coding: utf-8 -*-

import logging
from apps.sp.models.Model import Model

log = logging.getLogger(__name__)


class Search(object):
    MESSAGE_ERR = ''
    TYPE_BASIC = 1
    TYPE_ADVANCE = 2

    def __init__(self):
        self._type_search = self.TYPE_BASIC
        self._params = {}
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

    def set_query(self):
        try:
            for param in self._params:
                models = Model.objects.filter()
        except Exception, e:
            log.exception(e.message)

    def search(self):
        try:
            pass
        except Exception, e:
            log.exception(e.message)
        return self._result


