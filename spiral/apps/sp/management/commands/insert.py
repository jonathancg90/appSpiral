from django.core.management.base import BaseCommand
from optparse import make_option
from apps.sp.tests.Helpers.data_helpers.criterion_category import CriterionCategoryHelper
from apps.common.insert_helper import CriterionHelper, CriterionDetailHelper
from apps.sp.models.CriterionCategory import CriterionCategory
from apps.sp.models.Criterion import Criterion


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
            self.insert_criterion_category()
            self.insert_criterion()
            self.insert_criterion_detail()

        if entity == 'criterion_category':
            self.insert_criterion_category()

        if entity == 'criterion':
            self.insert_criterion()

        if entity == 'criterion_detail':
            self.insert_criterion_detail()

    def insert_criterion_category(self):
        if self.data_delete:
            CriterionCategory.objects.all().delete()
            self.stdout.write('delete data: criterion category. \n')
        else:
            if CriterionCategory.objects.all().count() == 0:
                criterion_category_helper = CriterionCategoryHelper()
                criterion_category_helper.set_data()
                criterion_category_helper.insert_data()
                self.stdout.write('Successfully inserted data: criterion category. \n')
            else:
                self.stdout.write('can not insert the data: criterion category. \n')

    def insert_criterion(self):
        if self.data_delete:
            Criterion.objects.all().delete()
            self.stdout.write('delete data: criterion. \n')
        else:
            criterion_helper = CriterionHelper()
            criterion_helper.insert_data()
            self.stdout.write('Successfully inserted data criterion. \n')

    def insert_criterion_detail(self):
        if self.data_delete:
            Criterion.objects.all().delete()
            self.stdout.write('delete data: criterion. \n')
        else:
            criterion_detail_helper = CriterionDetailHelper()
            criterion_detail_helper.insert_data()
            self.stdout.write('Successfully inserted data criterion detail. \n')
