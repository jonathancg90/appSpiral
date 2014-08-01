
from apps.common.insert_helper import CountryHelper
from apps.common.insert_helper import FeatureHelper

from apps.sp.tests.Helpers.data_helpers.entry import EntryHelper
from apps.sp.tests.Helpers.data_helpers.brand import BrandHelper
from apps.sp.tests.Helpers.data_helpers.commercial import CommercialHelper
from apps.sp.tests.Helpers.data_helpers.project import ProjectHelper
from apps.sp.tests.Helpers.data_helpers.model import ModelHelper
from apps.sp.tests.Helpers.data_helpers.model import ModelFeatureHelper
from apps.sp.tests.Helpers.data_helpers.user import SuperAdminHelper
from apps.sp.tests.Helpers.data_helpers.group import GroupHelper
from apps.sp.tests.Helpers.data_helpers.type_client import TypeClientHelper
from apps.sp.tests.Helpers.data_helpers.client import ClientHelper
from apps.common.insert_helper import TypeCastingHelper
from apps.common.insert_helper import CurrencyHelper
from apps.common.insert_helper import TypePhotoCastingHelper
from apps.common.insert_helper import PhotoUseHelper
from apps.common.insert_helper import TypeEventHelper
from apps.common.insert_helper import BroadcastHelper


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
        self.super_admin_helper = SuperAdminHelper()
        self.group_helper = GroupHelper()
        self.type_client_helper = TypeClientHelper()
        self.client_helper = ClientHelper()
        self.type_casting_helper = TypeCastingHelper()
        self.currency_helper = CurrencyHelper()
        self.type_photo_casting_helper = TypePhotoCastingHelper()
        self.photo_use_helper = PhotoUseHelper()
        self.type_event_helper = TypeEventHelper()
        self.broadcast_helper = BroadcastHelper()

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

        self.super_admin_helper.set_data()
        self.super_admin_helper.insert_data()

        self.group_helper.set_data()
        self.group_helper.insert_data()

        self.type_client_helper.set_data()
        self.type_client_helper.insert_data()

        self.client_helper.set_data()
        self.client_helper.insert_data()
        self.client_helper.insert_type()

        self.type_casting_helper.insert_data()

        self.currency_helper.insert_data()

        self.type_photo_casting_helper.insert_data()

        self.photo_use_helper.insert_data()

        self.type_event_helper.insert_data()

        self.broadcast_helper.insert_data()