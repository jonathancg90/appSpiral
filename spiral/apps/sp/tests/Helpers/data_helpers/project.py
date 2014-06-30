import datetime

from apps.sp.management.commands_helpers.insert import InsertHelperMixin
from apps.sp.models.Project import Project
from apps.sp.models.Commercial import Commercial


class ProjectHelper(InsertHelperMixin):
    entity = Project

    def set_data(self):
        self.objects_to_insert = [
            {
                'project_code':'13-06M040',
                'project_name':'Coca cola navidad',
                'line_productions':Project.LINE_CASTING,
                'start_productions': datetime.date.today(),
                'budget': 400
            },
            {
                'project_code':'13-06M050',
                'project_name':'Claro 4G',
                'line_productions':Project.LINE_CASTING,
                'start_productions': datetime.date.today(),
                'budget': 200
            },
            {
                'project_code':'13-06M060',
                'project_name':'Cristal Verano',
                'line_productions':Project.LINE_CASTING,
                'start_productions': datetime.date.today(),
                'budget': 300
            },
            {
                'project_code':'13-06M070',
                'project_name':'Bcp Multiservicio',
                'line_productions':Project.LINE_CASTING,
                'start_productions': datetime.date.today(),
                'budget': 100
            }
        ]