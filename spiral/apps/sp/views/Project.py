from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from apps.sp.forms.Project import ProjectForm
from apps.sp.models.Project import Project


class ProjectCreateView(CreateView):
    form_class = ProjectForm
    template = 'templates/CRUD.html'
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super(ProjectCreateView,self).get_context_data(**kwargs)
        context['action'] = 'create'
        return context


class ProjectUpdateView(UpdateView):
    form_class = ProjectForm
    template = 'templates/CRUD.html'
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super(ProjectUpdateView,self).get_context_data(**kwargs)
        context['action'] = 'update'
        return context

class ProjectDeleteView(DeleteView):
    model = Project
    template = 'templates/CRUD.html'
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super(ProjectUpdateView,self).get_context_data(**kwargs)
        context['action'] = 'delete'
        return context

class ProjectListView(ListView):
    model = Project
    template = ''