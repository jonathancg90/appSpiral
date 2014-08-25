import datetime

from apps.sp.management.commands_helpers.insert import InsertHelperMixin
from apps.sp.models.Project import Project


class ProjectHelper(InsertHelperMixin):
    entity = Project

    def set_data(self):
        self.objects_to_insert = [
            {
                'line_productions':Project.LINE_CASTING,
                'start_productions': datetime.date.today(),
                'end_productions': datetime.date.today(),
                'budget': 400
            },
            {
                'line_productions':Project.LINE_CASTING,
                'start_productions': datetime.date.today(),
                'end_productions': datetime.date.today(),
                'budget': 200
            },
            {
                'line_productions':Project.LINE_CASTING,
                'start_productions': datetime.date.today(),
                'end_productions': datetime.date.today(),
                'budget': 300
            },
            {
                'line_productions':Project.LINE_CASTING,
                'start_productions': datetime.date.today(),
                'end_productions': datetime.date.today(),
                'budget': 100
            }
        ]