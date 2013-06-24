# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from apps.common.view import SearchFormMixin
from apps.sp.forms.Commercial import CommercialCreateForm, CommercialUpdateForm,\
    CommercialFiltersForm
from apps.common.view import JSONResponseMixin
from apps.sp.models.Project import Project
from apps.sp.models.Commercial import Commercial


class CommercialListView(SearchFormMixin, ListView):
    model = Commercial
    template_name = 'panel/commercial/commercial_list.html'
    search_form_class = CommercialFiltersForm
    paginate_by = settings.PANEL_PAGE_SIZE
    filtering = {
        'name': SearchFormMixin.ALL,
        'brand__entry': SearchFormMixin.ALL,
        'brand_id': SearchFormMixin.ALL,
    }

    def _set_filter_entry(self, qs):
        entry_id = str(self.request.GET.get('brand__entry', ''))
        if entry_id.isdigit():
            qs = qs.filter(brand__entry=entry_id)
        return qs

    def get_queryset(self):
        qs = super(CommercialListView, self).get_queryset()
        qs = self._set_filter_entry(qs)
        return qs

    def get_search_form(self, form_class):
        entry_id = self.request.GET.get('brand__entry', None)
        form = super(CommercialListView, self).get_search_form(form_class)
        if entry_id:
            form.set_brand(entry_id)
        return form


class CommercialCreateView(CreateView):
    model = Commercial
    form_class = CommercialCreateForm
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
            project = Project.objects.get(project_code=project_code)
            self.object.project = project
            self.object.save()
            return super(CommercialCreateView, self).form_valid(form)

        else:
            project = Project()
            project.project_code = project_code
            project.name = project_code
            project.project_type = Project.TYPE_CASTING
            project.save()
            self.object.project = project
            self.object.save()
            return super(CommercialCreateView, self).form_valid(form)

    def validate_project_code(self, project_code):
        try:
            Project.objects.get(project_code=project_code)
            return True
        except:
            return False

    def get_form(self, form_class):
        form = super(CommercialCreateView, self).get_form(form_class)
        _entry_id = self.request.POST.get('entry_id', None)
        try:
            if _entry_id:
                form.set_brand(_entry_id)
            return form
        except AttributeError:
            return form

    def get_success_url(self):
        return reverse('commercial_list')


class CommercialUpdateView(UpdateView):
    model = Commercial
    form_class = CommercialUpdateForm
    template_name = 'panel/commercial/update.html'
    success_url = 'commercial_list'

    def get_form(self, form_class):
        form = super(CommercialUpdateView, self).get_form(form_class)
        pk = self.kwargs.get('pk')
        commercial = Commercial.objects.get(pk=pk)
        form.fields['project'].initial = commercial.project.project_code
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        project_code = self.request.POST.get('project')
        if self.validate_project_code(project_code):
            project = Project.objects.get(project_code=project_code)
            self.object.project = project
            self.object.save()
            return super(CommercialUpdateView, self).form_valid(form)

        else:
            project = Project()
            project.project_code = project_code
            project.name = project_code
            project.project_type = Project.TYPE_CASTING
            project.save()
            self.object.project = project
            self.object.save()
            return super(CommercialUpdateView, self).form_valid(form)

    def validate_project_code(self, project_code):
        try:
            Project.objects.get(project_code=project_code)
            return True
        except:
            return False

    def get_success_url(self):
        return reverse('commercial_list')


class CommercialDeleteView(DeleteView):
    model = Commercial
    template_name = 'panel/commercial/delete.html'
    success_url = 'commercial_list'

    def get_context_data(self, **kwargs):
        context = super(CommercialDeleteView,self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('commercial_list')


class CommercialByBrandIdJson(JSONResponseMixin, ListView):
    model = Commercial

    def get_queryset(self):
        band_id = self.kwargs.get('brand', 0)
        qs = Commercial.objects.filter(brand_id=band_id)
        return qs

    def get_context_data(self, **kwargs):
        data = {}
        brand = self.get_queryset().values('id', 'name')
        data['commercial'] = [item for item in brand]
        return data