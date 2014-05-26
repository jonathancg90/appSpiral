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
                "realized":datetime.datetime.utcnow().replace(tzinfo=utc),
                "brand": Brand.objects.get(name="Coca Cola"),
                "project":Project.objects.get(project_code="13-06M040")
            },
            {
                "name": "Claro 4G",
                "realized":datetime.datetime.utcnow().replace(tzinfo=utc),
                "brand":Brand.objects.get(name="Claro"),
                "project":Project.objects.get(project_code="13-06M050")
            },
            {
                "name": "Cristal Verano",
                "realized":datetime.datetime.utcnow().replace(tzinfo=utc),
                "brand":Brand.objects.get(name="Cristal"),
                "project":Project.objects.get(project_code="13-06M060")
            },
            {
                "name": "Bcp Multiservicio",
                "realized":datetime.datetime.utcnow().replace(tzinfo=utc),
                "brand":Brand.objects.get(name="Bcp"),
                "project":Project.objects.get(project_code="13-06M070")
            },
        ]