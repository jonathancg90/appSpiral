from django.core.management.base import BaseCommand
from optparse import make_option
from apps.sp.models.Feature import Feature
from apps.sp.models.Country import Country
from apps.sp.models.Currency import Currency
from apps.sp.models.Client import TypeClient
from apps.sp.models.Casting import TypeCasting
from apps.common.insert_helper import CountryHelper
from apps.common.insert_helper import TypeClientHelper
from apps.common.insert_helper import TypeCastingHelper
from apps.common.insert_helper import FeatureHelper
from apps.common.insert_helper import DataTestHelper
from apps.common.insert_helper import CurrencyHelper

class Command(BaseCommand):
    data_delete = False

    option_list = BaseCommand.option_list + (
        make_option('--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Delete data'),
        )

    def handle(self, *args, **options):
        entity = args[0]

        if options['delete']:
            self.data_delete = True

        if entity == 'all':
            self.insert_features()
            self.insert_countries()
            self.insert_type_casting()
            self.insert_type_client()
            self.insert_currency()

        if entity == 'country':
            self.insert_countries()

        if entity == 'feature':
            self.insert_features()

        if entity == 'type_client':
            self.insert_type_client()

        if entity == 'type_casting':
            self.insert_type_casting()

        if entity == 'currency':
            self.insert_currency()

        if entity == 'test_data':
            self.insert_data_test()

    def insert_features(self):
        if self.data_delete:
            Feature.objects.all().delete()
            self.stdout.write('delete data: feature - feature_value. \n')
        else:
            if Feature.objects.all().count() == 0:
                feature_helper = FeatureHelper()
                feature_helper.insert_data()
                self.stdout.write('Successfully inserted data: feature. \n')
            else:
                self.stdout.write('can not insert the data: feature. \n')

    def insert_countries(self):
        if self.data_delete:
            Country.objects.all().delete()
            self.stdout.write('delete data: country. \n')
        else:
            if Country.objects.all().count() == 0:
                country_helper = CountryHelper()
                country_helper.insert_data()
                self.stdout.write('Successfully inserted data: country. \n')
            else:
                self.stdout.write('can not insert the data: country. \n')

    def insert_type_client(self):
        if self.data_delete:
            TypeClient.objects.all().delete()
            self.stdout.write('delete data: type client. \n')
        else:
            if TypeClient.objects.all().count() == 0:
                type_client_helper = TypeClientHelper()
                type_client_helper.insert_data()
                self.stdout.write('Successfully inserted data: type client. \n')
            else:
                self.stdout.write('can not insert the data: type client. \n')

    def insert_type_casting(self):
        if self.data_delete:
            TypeCasting.objects.all().delete()
            self.stdout.write('delete data: type casting. \n')
        else:
            if TypeCasting.objects.all().count() == 0:
                type_casting_helper = TypeCastingHelper()
                type_casting_helper.insert_data()
                self.stdout.write('Successfully inserted data: type casting. \n')
            else:
                self.stdout.write('can not insert the data: type casting. \n')

    def insert_currency(self):
        if self.data_delete:
            Currency.objects.all().delete()
            self.stdout.write('delete data:  currency. \n')
        else:
            if Currency.objects.all().count() == 0:
                currency_helper = CurrencyHelper()
                currency_helper.insert_data()
                self.stdout.write('Successfully inserted data: currency. \n')
            else:
                self.stdout.write('can not insert the data: currency. \n')

    def insert_data_test(self):
        if self.data_delete:
            self.stdout.write('Command not exists in data test. \n')
        else:
            data_test_helper = DataTestHelper()
            data_test_helper.insert_data()
            self.stdout.write('Successfully inserted data: test data. \n')