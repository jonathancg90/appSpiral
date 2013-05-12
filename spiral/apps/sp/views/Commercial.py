# -*- coding: utf-8 -*-
from django.conf import settings

from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from apps.common.view import SearchFormMixin
from apps.sp.forms.Commercial import CommercialForm, CommercialFiltersForm
from apps.sp.models.Project import Project
from apps.sp.models.Commercial import Commercial


class CommercialCreateView(CreateView):
    model = Commercial
    form_class = CommercialForm
    template_name = 'panel/commercial/create.html'
    success_url = 'commercial_list'

    def get_context_data(self, **kwargs):
        context = super(CommercialCreateView,self).get_context_data(**kwargs)
        context['action'] = 'create'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        project_code = self.request.POST.get('project')
        if self.validate_project_code(project_code):
            project_id = Project.objects.get(project_code=project_code)
            self.object.project_id = project_id
            self.object.save()
            return super(CommercialCreateView, self).form_valid(form)

        else:
            project = Project()
            project.project_code = project_code
            project.name = project_code
            project.project_type = Project.TYPE_CASTING
            project.save()
            self.object.project_id = project
            self.object.save()
            return super(CommercialCreateView, self).form_valid(form)

    def validate_project_code(self, project_code):
        try:
            Project.objects.get(project_code=project_code)
            return True
        except:
            return False





class CommercialUpdateView(UpdateView):
    model = Commercial
    form_class = CommercialForm
    template_name = 'panel/commercial/update.html'
    success_url = 'commercial_list'

    def get_form(self, form_class):
        form = super(CommercialUpdateView, self).get_form(form_class)
        pk = self.kwargs.get('pk')
        commercial = Commercial.objects.get(pk=pk)
        form.fields['project'].initial = commercial.project_id.project_code
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        project_code = self.request.POST.get('project')
        if self.validate_project_code(project_code):
            project_id = Project.objects.get(project_code=project_code)
            self.object.project_id = project_id
            self.object.save()
            return super(CommercialUpdateView, self).form_valid(form)

        else:
            project = Project()
            project.project_code = project_code
            project.name = project_code
            project.project_type = Project.TYPE_CASTING
            project.save()
            self.object.project_id = project
            self.object.save()
            return super(CommercialUpdateView, self).form_valid(form)

    def validate_project_code(self, project_code):
        try:
            Project.objects.get(project_code=project_code)
            return True
        except:
            return False

class CommercialDeleteView(DeleteView):
    model = Commercial
    template_name = 'panel/commercial/delete.html'
    success_url = 'commercial_list'

    def get_context_data(self, **kwargs):
        context = super(CommercialDeleteView,self).get_context_data(**kwargs)
        return context

class CommercialListView(SearchFormMixin, ListView):
    model = Commercial
    template_name = 'panel/commercial/commercial_list.html'
    search_form_class = CommercialFiltersForm
    paginate_by = settings.PANEL_PAGE_SIZE
    filtering = {
        'name': SearchFormMixin.ALL,
        'entry_id': SearchFormMixin.ALL,
        'brand_id': SearchFormMixin.ALL,
    }

