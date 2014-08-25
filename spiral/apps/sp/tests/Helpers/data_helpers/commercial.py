# -*- encoding: utf-8 -*-
import datetime
from django.utils.timezone import utc
from apps.sp.management.commands_helpers.insert import InsertHelperMixin
from apps.sp.models.Commercial import Commercial
from apps.sp.models.Brand import Brand
from apps.sp.models.Project import Project


class CommercialHelper(InsertHelperMixin):
    entity = Commercial

    def set_data(self):
        self.objects_to_insert = [
            {
                "name": "Coca Cola Navidad",
                "brand": Brand.objects.get(name="Coca Cola"),
            },
            {
                "name": "Claro 4G",
                "brand":Brand.objects.get(name="Claro"),
            },
            {
                "name": "Cristal Verano",
                "brand":Brand.objects.get(name="Cristal"),
            },
            {
                "name": "Bcp Multiservicio",
                "brand":Brand.objects.get(name="Bcp"),
            },
        ]