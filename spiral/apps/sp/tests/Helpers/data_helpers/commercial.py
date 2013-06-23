# -*- encoding: utf-8 -*-
from apps.sp.management.commands_helpers.insert import InsertHelperMixin
from apps.sp.models.Commercial import Commercial
from apps.sp.models.Brand import Brand


class CommercialHelper(InsertHelperMixin):
    entity = Commercial

    def set_data(self):
        self.objects_to_insert = [
            {
                "name": "Coca Cola Navidad",
                "realized":"12-06-2013",
                "brand": Brand.objects.get(name="Coca Cola"),
                "project":"13-06M040"
            },
            {
                "name": "Claro 4G",
                "realized":"23-06-2013",
                "brand":Brand.objects.get(name="Claro"),
                "project":"13-06M050"
            },
            {
                "name": "Cristal Verano",
                "realized":"14-06-2013",
                "brand":Brand.objects.get(name="Cristal"),
                "project":"13-06M060"
            },
            {
                "name": "Bcp Multiservicio",
                "realized":"12-06-2013",
                "brand":Brand.objects.get(name="Bcp"),
                "project":"13-06M070"
            },
        ]