import datetime

from apps.sp.management.commands_helpers.insert import InsertHelperMixin
from apps.sp.models.Project import Project


class ProjectHelper(InsertHelperMixin):
    entity = Project

    def set_data(self):
        self.objects_to_insert = [
            {
                'project_code':'13-06M040',
                'line_productions':Project.LINE_CASTING,
                'start_productions': datetime.date.today(),
                'end_productions': datetime.date.today(),
                'budget': 400
            },
            {
                'project_code':'13-06M050',
                'line_productions':Project.LINE_CASTING,
                'start_productions': datetime.date.today(),
                'end_productions': datetime.date.today(),
                'budget': 200
            },
            {
                'project_code':'13-06M060',
                'line_productions':Project.LINE_CASTING,
                'start_productions': datetime.date.today(),
                'end_productions': datetime.date.today(),
                'budget': 300
            },
            {
                'project_code':'13-06M070',
                'line_productions':Project.LINE_CASTING,
                'start_productions': datetime.date.today(),
                'end_productions': datetime.date.today(),
                'budget': 100
            }
        ]