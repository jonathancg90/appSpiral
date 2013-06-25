# -*- encoding: utf-8 -*-
from apps.sp.management.commands_helpers.insert import InsertHelperMixin
from apps.sp.models.CriterionCategory import CriterionCategory


class CriterionCategoryHelper(InsertHelperMixin):
    entity = CriterionCategory

    def set_data(self):
        self.objects_to_insert = [
            {
                "description": "Descriptivos",
            },
            {
                "description": "Fotografico",
            },
            {
                "description": "Video",
            },
            {
                "description": "Evaluacion",
            },
            {
                "description": "Multimedia",
            }
        ]