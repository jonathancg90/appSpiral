from apps.sp.management.commands_helpers.insert import InsertHelperMixin
from apps.sp.models.Project import Project


class ProjectHelper(InsertHelperMixin):
    entity = Project

    def set_data(self):
        self.objects_to_insert = [
            {
                'project_code':'13-06M040',
                'project_name':'Coca cola navidad',
                'project_type':Project.TYPE_CASTING
            },
            {
                'project_code':'13-06M050',
                'project_name':'Claro 4G',
                'project_type':Project.TYPE_CASTING
            },
            {
                'project_code':'13-06M060',
                'project_name':'Cristal Verano',
                'project_type':Project.TYPE_CASTING
            },
            {
                'project_code':'13-06M070',
                'project_name':'Bcp Multiservicio',
                'project_type':Project.TYPE_CASTING
            }
        ]