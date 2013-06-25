# -*- coding: utf-8 -*-
import json
from django.conf import settings
from apps.sp.models.Criterion import Criterion, CriterionDetail
from apps.sp.models.CriterionCategory import CriterionCategory


class ReaderJsonHelper(object):

    def json_reader(self, json_file):
        ROOT_PATH = settings.ROOT_PATH
        file_path = ROOT_PATH + '/apps/common/db_data/%s.json' %json_file
        file = open(file_path, 'r')
        json_data = json.load(file)
        file.close()
        return json_data


class ReaderTxtHelper(object):

    def data_parse(self, file):
        txt = '/apps/common/db_data/%s.txt' %file

        ROOT_PATH = settings.ROOT_PATH
        file_path = ROOT_PATH + txt

        file = open(file_path, 'r')
        line = True

        while line:
            line = file.readline().strip()

            if len(line) < 1 or line[0] == '#':
                continue

            yield [e.strip() for e in line.split('\t')]


class CriterionHelper(ReaderTxtHelper):

    def insert_data(self):
        for data in self.data_parse('criterion'):
            try:
                criterion = Criterion()
                criterion.cri_cod = data[0]
                criterion.description = data[1]
                criterion.criterion_category = CriterionCategory.objects.get(
                    description=data[2]
                )
                criterion.multi = self.get_multi_value(data[3])
                criterion.save()
            except:
                print('can not exist '+data[2])

    def get_multi_value(self, value):
        if value == 'V':
            return True
        else:
            return False


class CriterionDetailHelper(ReaderTxtHelper):

    def insert_data(self):
        for data in self.data_parse('criterion_detail'):
            try:
                criterion_detail = CriterionDetail()
                criterion_detail.criterion = Criterion.objects.get(
                    cri_cod=data[0]
                )
                criterion_detail.cri_item = data[1]
                criterion_detail.description = data[2]
                criterion_detail.save()
            except:
                print('can not exist '+data[0])