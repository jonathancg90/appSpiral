
from apps.common.insert_helper import CountryHelper
from apps.common.insert_helper import FeatureHelper

from apps.sp.tests.Helpers.data_helpers.entry import EntryHelper
from apps.sp.tests.Helpers.data_helpers.brand import BrandHelper
from apps.sp.tests.Helpers.data_helpers.commercial import CommercialHelper
from apps.sp.tests.Helpers.data_helpers.project import ProjectHelper
from apps.sp.tests.Helpers.data_helpers.model import ModelHelper
from apps.sp.tests.Helpers.data_helpers.model import ModelFeatureHelper


class InsertDataHelper(object):

    def __init__(self):
        self.country_helper = CountryHelper()
        self.feature_helper = FeatureHelper()

        self.entry_helper = EntryHelper()
        self.brand_helper = BrandHelper()
        self.commercial_helper = CommercialHelper()
        self.project_helper = ProjectHelper()
        self.model_helper = ModelHelper()
        self.model_feature_helper = ModelFeatureHelper()

    def run(self):
        self.entry_helper.set_data()
        self.entry_helper.insert_data()

        self.brand_helper.set_data()
        self.brand_helper.insert_data()

        self.project_helper.set_data()
        self.project_helper.insert_data()

        self.commercial_helper.set_data()
        self.commercial_helper.insert_data()

        self.country_helper.insert_data()

        self.model_helper.set_data()
        self.model_helper.insert_data()

        self.feature_helper.insert_data()

        self.model_feature_helper.set_data()
        self.model_feature_helper.insert_data()