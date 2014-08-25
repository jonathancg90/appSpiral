from django.core.management.base import BaseCommand
from optparse import make_option
from apps.sp.models.Feature import Feature
from apps.sp.models.Country import Country
from apps.sp.models.Currency import Currency
from apps.sp.models.Client import TypeClient
from apps.sp.models.Representation import TypeEvent
from apps.sp.models.Casting import TypeCasting
from apps.sp.models.PhotoCasting import TypePhotoCasting
from apps.sp.models.PhotoCasting import UsePhotos
from apps.sp.models.Broadcast import Broadcast
from apps.sp.models.Contract import TypeContract
from apps.sp.models.PictureDetail import MediaFeature
from apps.common.insert_helper import CountryHelper
from apps.common.insert_helper import TypeClientHelper
from apps.common.insert_helper import TypeCastingHelper
from apps.common.insert_helper import TypePhotoCastingHelper
from apps.common.insert_helper import FeatureHelper
from apps.common.insert_helper import DataTestHelper
from apps.common.insert_helper import BroadcastHelper
from apps.common.insert_helper import CurrencyHelper
from apps.common.insert_helper import TypeEventHelper
from apps.common.insert_helper import MediaFeatureHelper
from apps.common.insert_helper import PhotoUseHelper
from apps.common.insert_helper import TypeContractHelper
from apps.sp.management.migration.Model import ModelProcessMigrate


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
            self.insert_type_photo_casting()
            self.insert_type_event()
            self.insert_photo_use()
            self.insert_broadcast()
            self.insert_type_contract()
            self.insert_media_feature()

        if entity == 'migration':
            self.migration_process()

        if entity == 'country':
            self.insert_countries()

        if entity == 'feature':
            self.insert_features()

        if entity == 'type_client':
            self.insert_type_client()

        if entity == 'type_casting':
            self.insert_type_casting()

        if entity == 'type_event':
            self.insert_type_event()

        if entity == 'type_contract':
            self.insert_type_contract()

        if entity == 'photo_use':
            self.insert_photo_use()

        if entity == 'type_photo_casting':
            self.insert_type_photo_casting()

        if entity == 'currency':
            self.insert_currency()

        if entity == 'broadcast':
            self.insert_broadcast()

        if entity == 'test_data':
            self.insert_data_test()

        if entity == 'media_feature':
            self.insert_media_feature()

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

    def insert_type_event(self):
        if self.data_delete:
            TypeEvent.objects.all().delete()
            self.stdout.write('delete data: type event. \n')
        else:
            if TypeEvent.objects.all().count() == 0:
                type_event_helper = TypeEventHelper()
                type_event_helper.insert_data()
                self.stdout.write('Successfully inserted data: type event. \n')
            else:
                self.stdout.write('can not insert the data: type event. \n')

    def insert_photo_use(self):
        if self.data_delete:
            UsePhotos.objects.all().delete()
            self.stdout.write('delete data: photo use. \n')
        else:
            if UsePhotos.objects.all().count() == 0:
                use_photos_helper = PhotoUseHelper()
                use_photos_helper.insert_data()
                self.stdout.write('Successfully inserted data: photo use. \n')
            else:
                self.stdout.write('can not insert the data: photo use. \n')

    def insert_type_photo_casting(self):
        if self.data_delete:
            TypePhotoCasting.objects.all().delete()
            self.stdout.write('delete data: type photo casting. \n')
        else:
            if TypePhotoCasting.objects.all().count() == 0:
                type_photo_casting_helper = TypePhotoCastingHelper()
                type_photo_casting_helper.insert_data()
                self.stdout.write('Successfully inserted data: type photo casting. \n')
            else:
                self.stdout.write('can not insert the data: type photo casting. \n')

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

    def insert_type_contract(self):
        if self.data_delete:
            TypeContract.objects.all().delete()
            self.stdout.write('delete data:  type contract. \n')
        else:
            if TypeContract.objects.all().count() == 0:
                type_contract_helper = TypeContractHelper()
                type_contract_helper.insert_data()
                self.stdout.write('Successfully inserted data: type contract. \n')
            else:
                self.stdout.write('can not insert the data: type contract. \n')

    def insert_media_feature(self):
        if self.data_delete:
            MediaFeature.objects.all().delete()
            self.stdout.write('delete data: media - feature. \n')
        else:
            if MediaFeature.objects.all().count() == 0:
                media_feature_helper = MediaFeatureHelper()
                media_feature_helper.insert_data()
                self.stdout.write('Successfully inserted data: media feature. \n')
            else:
                self.stdout.write('can not insert the data: media feature. \n')

    def insert_broadcast(self):
        if self.data_delete:
            Broadcast.objects.all().delete()
            self.stdout.write('delete data: broadcast. \n')
        else:
            if Broadcast.objects.all().count() == 0:
                broadcast_helper = BroadcastHelper()
                broadcast_helper.insert_data()
                self.stdout.write('Successfully inserted data: broadcast. \n')
            else:
                self.stdout.write('can not insert the data: broadcast. \n')

    def insert_data_test(self):
        if self.data_delete:
            self.stdout.write('Command not exists in data test. \n')
        else:
            data_test_helper = DataTestHelper()
            data_test_helper.insert_data()
            self.stdout.write('Successfully inserted data: test data. \n')


    def migration_process(self):
        model_process_migrate = ModelProcessMigrate()
        model_process_migrate.start_migration()
