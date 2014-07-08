from django.core.management.base import BaseCommand
from optparse import make_option
from apps.sp.models.Feature import Feature
from apps.sp.models.Country import Country
from apps.sp.models.Client import TypeClient
from apps.common.insert_helper import CountryHelper
from apps.common.insert_helper import TypeClientHelper
from apps.common.insert_helper import FeatureHelper

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

        if entity == 'country':
            self.insert_countries()

        if entity == 'feature':
            self.insert_features()

        if entity == 'type_client':
            self.insert_type_client()

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
                country_helper = TypeClientHelper()
                country_helper.insert_data()
                self.stdout.write('Successfully inserted data: type client. \n')
            else:
                self.stdout.write('can not insert the data: type client. \n')
