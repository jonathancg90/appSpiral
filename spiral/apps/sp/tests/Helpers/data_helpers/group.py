# -*- encoding: utf-8 -*-
import uuid
from apps.sp.management.commands_helpers.insert import InsertHelperMixin
from django.contrib.auth.models import Group


class GroupHelper(InsertHelperMixin):
    entity = Group

    def set_data(self):
        self.objects_to_insert = [
            {
                "name": 'evento',
            },
            {
                "name": 'produccion',
            }
        ]