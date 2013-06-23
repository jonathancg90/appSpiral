from apps.sp.tests.Helpers.data_helpers.entry import EntryHelper
from apps.sp.tests.Helpers.data_helpers.brand import BrandHelper
from apps.sp.tests.Helpers.data_helpers.commercial import CommercialHelper


class InsertDataHelper(object):

    def __init__(self):
        self.entry_helper = EntryHelper()
        self.brand_helper = BrandHelper()
        self.commercial_helper = CommercialHelper()

    def set_data(self):
        self.entry_helper.set_data()
        self.brand_helper.set_data()
        self.commercial_helper.set_data()

    def insert_data(self):
        self.entry_helper.insert_data()
        self.brand_helper.insert_data()
        self.commercial_helper.insert_data()

    def insert_data_helper(self):
        #Insertar toda la data de prueba para el proyecto#
        self.set_data()
        self.insert_data()
