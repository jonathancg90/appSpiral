# -*- encoding: utf-8 -*-
from apps.sp.management.commands_helpers.insert import InsertHelperMixin
from apps.sp.models.Client import TypeClient


class TypeClientHelper(InsertHelperMixin):
    entity = TypeClient

    def set_data(self):
        self.objects_to_insert = [
            {
                "name": 'Productora',
            },
            {
                "name": 'Realizadora',
            },
            {
                "name": 'Agencia',
            }
        ]