from apps.sp.tests.Helpers.data_helpers.entry import EntryHelper
from apps.sp.tests.Helpers.data_helpers.brand import BrandHelper
from apps.sp.tests.Helpers.data_helpers.commercial import CommercialHelper
from apps.sp.tests.Helpers.data_helpers.project import ProjectHelper


class InsertDataHelper(object):

    def __init__(self):
        self.entry_helper = EntryHelper()
        self.brand_helper = BrandHelper()
        self.commercial_helper = CommercialHelper()
        self.project_helper = ProjectHelper()

    def insert_data_helper(self):
        self.entry_helper.set_data()
        self.entry_helper.insert_data()

        self.brand_helper.set_data()
        self.brand_helper.insert_data()

        self.project_helper.set_data()
        self.project_helper.insert_data()

        self.commercial_helper.set_data()
        self.commercial_helper.insert_data()