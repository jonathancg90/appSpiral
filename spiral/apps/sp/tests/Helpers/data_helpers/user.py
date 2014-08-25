# -*- encoding: utf-8 -*-
import uuid
from apps.sp.management.commands_helpers.insert import InsertHelperMixin
from django.contrib.auth.models import User


class SuperAdminHelper(InsertHelperMixin):
    entity = User

    def set_data(self):
        self.objects_to_insert = [
            {
                "username": 'admin',
                "email": 'admin@gmail.com',
                "password": uuid.uuid4().hex,
                "is_superuser": True
            }
        ]