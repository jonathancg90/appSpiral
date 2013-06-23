# -*- encoding: utf-8 -*-
from apps.sp.management.commands_helpers.insert import InsertHelperMixin
from apps.sp.models.Entry import Entry


class EntryHelper(InsertHelperMixin):
    entity = Entry

    def set_data(self):
        self.objects_to_insert = [
            {
                "name": "Gaseosa"
            },
            {
                "name": "Bancos"
            },
            {
                "name": "Telefonia"
            },
            {
                "name": "Cervezas"
            },
            {
                "name": "Embutidos"
            }
        ]