from apps.sp.management.commands_helpers.insert import InsertHelperMixin
from apps.sp.models.Brand import Brand
from apps.sp.models.Entry import Entry


class BrandHelper(InsertHelperMixin):
    entity = Brand

    def set_data(self):
        self.objects_to_insert = [
            {
                "name": "Coca Cola",
                "entry": Entry.objects.get(name="Gaseosa")
            },
            {
                "name": "Sprite",
                "entry":Entry.objects.get(name="Gaseosa")
            },
            {
                "name": "Bcp",
                "entry":Entry.objects.get(name="Bancos")
            },
            {
                "name": "Movistar",
                "entry":Entry.objects.get(name="Telefonia")
            },
            {
                "name": "BBVA",
                "entry":Entry.objects.get(name="Bancos")
            },
            {
                "name": "Otto Kunz",
                "entry":Entry.objects.get(name="Embutidos")
            },
            {
                "name": "Cuzqueña",
                "entry":Entry.objects.get(name="Cervezas")
            },
            {
                "name": "Cristal",
                "entry":Entry.objects.get(name="Cervezas")
            },
            {
                "name": "Claro",
                "entry":Entry.objects.get(name="Telefonia")
            }
        ]


