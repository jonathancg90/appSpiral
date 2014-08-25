# -*- coding: utf-8 -*-

import json

import datetime
from django.conf import settings
from django.core.cache import cache
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from apps.common.view import SearchFormMixin
from apps.sp.forms.Commercial import CommercialCreateForm, CommercialUpdateForm,\
    CommercialFiltersForm
from apps.common.view import JSONResponseMixin
from apps.sp.models.Project import Project
from apps.sp.cache.CleanCache import CleanCache
from apps.sp.models.Entry import Entry
from apps.sp.models.Brand import Brand
from apps.sp.models.Commercial import Commercial, CommercialDateDetail
from apps.common.view import LoginRequiredMixin, PermissionRequiredMixin


class CommercialListView(LoginRequiredMixin, PermissionRequiredMixin,
                         SearchFormMixin, ListView):
    model = Commercial
    template_name = 'panel/commercial/commercial_list.html'
    search_form_class = CommercialFiltersForm
    paginate_by = settings.PANEL_PAGE_SIZE
    filtering = {
        'name': SearchFormMixin.ALL,
        'brand__entry': SearchFormMixin.ALL,
        'brand_id': SearchFormMixin.ALL,
    }
    cache_status = True

    def set_cache_status(self, status):
        self.cache_status = status

    def _set_filter_entry(self, qs):
        entry_id = str(self.request.GET.get('brand__entry', ''))
        if entry_id.isdigit():
            qs = qs.filter(brand__entry=entry_id)
        return qs

    def get_list(self, qs):
        data = []
        qs = qs.select_related('brand', 'brand__entry')
        qs = self._set_filter_entry(qs)
        for commercial in qs:
            data.append({
                'pk': commercial.id,
                'id': commercial.id,
                'name': commercial.name,
                'project': commercial.project,
                'realized': commercial.realized,
                'brand': commercial.brand.name,
                'entry': commercial.brand.entry.name
            })
        return data

    def get_queryset(self):
        options = {
            'brand_id': self.request.GET.get('brand_id', ''),
            'brand__entry': self.request.GET.get('brand__entry', ''),
            'name': self.request.GET.get('name__icontains', ''),
            'page': self.request.GET.get('page', '')
        }
        if settings.APPLICATION_CACHE and self.cache_status:
            str(self.request.GET.get('brand__entry', ''))

            if cache.hexists(Commercial.get_commercial_tag(), options):
                data = json.loads(cache.hget('commercial_list', options))
            else:
                qs = super(CommercialListView, self).get_queryset()
                data = self.get_list(qs)
                cache.hset(Commercial.get_commercial_tag(), options, json.dumps(data))
        else:
            qs = super(CommercialListView, self).get_queryset()
            data = self.get_list(qs)
        return data

    def get_search_form(self, form_class):
        entry_id = self.request.GET.get('brand__entry', None)
        form = super(CommercialListView, self).get_search_form(form_class)
        if entry_id:
            form.set_brand(entry_id)
        return form

    def get_context_data(self, **kwargs):
        context = super(CommercialListView, self).get_context_data(**kwargs)
        context['menu'] = 'maintenance'
        return context


class CommercialCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                           CreateView):
    model = Commercial
    form_class = CommercialCreateForm
    template_name = 'panel/commercial/create.html'
    success_url = 'commercial_list'
    permissions = {
        "permission": ('sp.add_commercial', ),
    }

    def get_context_data(self, **kwargs):
        context = super(CommercialCreateView,self).get_context_data(**kwargs)
        context['action'] = 'create'
        context['menu'] = 'maintenance'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        dataPost = self.request.POST
        self.object.save()
        for data in dataPost:
            if 'realized' in data:
                try:
                    realized = datetime.datetime.strptime(dataPost.get(data), '%d/%m/%Y').strftime('%Y-%m-%d')
                    detail = CommercialDateDetail()
                    detail.date = realized
                    self.object.commercial_date_detail_set.add(detail)
                except:
                    pass
        if settings.APPLICATION_CACHE:
            clean_cache = CleanCache()
            clean_cache.set_cache_result_tag(Commercial.get_commercial_tag())
            clean_cache.set_model(Commercial)
            clean_cache.update_cache_by_id([self.object.id], CleanCache.MODE_INSERT)
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


class CommercialUpdateView(LoginRequiredMixin, PermissionRequiredMixin,
                           UpdateView):
    model = Commercial
    form_class = CommercialUpdateForm
    template_name = 'panel/commercial/update.html'
    success_url = 'commercial_list'
    permissions = {
        "permission": ('sp.change_commercial', ),
    }

    def get_form(self, form_class):
        form = super(CommercialUpdateView, self).get_form(form_class)
        _entry_id = self.request.POST.get('entry_id', None)
        try:
            if _entry_id:
                form.cleaned_data['entry_id'] = Entry.objects.get(pk=_entry_id)
                form.set_entry(_entry_id)
                form.set_brand(_entry_id)
            else:
                form.set_entry(self.object.brand.entry.id)
            return form
        except AttributeError:
            return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        dataPost = self.request.POST
        self.object.commercial_date_detail_set.all().delete()
        self.object.save()
        for data in dataPost:
            if 'realized' in data:
                try:
                    realized = datetime.datetime.strptime(dataPost.get(data), '%d/%m/%Y').strftime('%Y-%m-%d')
                    detail = CommercialDateDetail()
                    detail.date = realized
                    self.object.commercial_date_detail_set.add(detail)
                except:
                    pass
        if settings.APPLICATION_CACHE:
            clean_cache = CleanCache()
            clean_cache.set_cache_result_tag(Commercial.get_commercial_tag())
            clean_cache.set_model(Commercial)
            clean_cache.update_cache_by_id([self.object.id], CleanCache.MODE_UPDATE)

        return super(CommercialUpdateView, self).form_valid(form)

    def validate_project_code(self, project_code):
        try:
            Project.objects.get(project_code=project_code)
            return True
        except:
            return False

    def get_details(self):
        data = []
        for detail in self.object.commercial_date_detail_set.all():
            data.append({
                "value": detail.date.strftime("%d/%m/%Y")
            })
        return data

    def get_context_data(self, **kwargs):
        context = super(CommercialUpdateView, self).get_context_data(**kwargs)
        context['dates'] = json.dumps(self.get_details())
        context['menu'] = 'maintenance'
        return context

    def get_success_url(self):
        return reverse('commercial_list')


class CommercialDeleteView(LoginRequiredMixin, PermissionRequiredMixin,
                           DeleteView):
    model = Commercial
    template_name = 'panel/commercial/delete.html'
    success_url = 'commercial_list'
    permissions = {
        "permission": ('sp.delete_commercial', ),
    }

    def get_context_data(self, **kwargs):
        context = super(CommercialDeleteView,self).get_context_data(**kwargs)
        context['menu'] = 'maintenance'
        return context

    def get_success_url(self):
        if settings.APPLICATION_CACHE:
            clean_cache = CleanCache()
            clean_cache.set_cache_result_tag(Commercial.get_commercial_tag())
            clean_cache.set_model(Commercial)
            clean_cache.update_cache_by_id([self.kwargs.get('pk')], CleanCache.MODE_DELETE)
        return reverse('commercial_list')


class CommercialByBrandIdJson(LoginRequiredMixin, PermissionRequiredMixin,
                              JSONResponseMixin, ListView):
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


class CommercialDataListView(LoginRequiredMixin, PermissionRequiredMixin,
                              JSONResponseMixin, ListView):
    model = Commercial

    def get_queryset(self):
        options = {
            'active': True,
        }
        if settings.APPLICATION_CACHE:
            tag = Commercial.get_commercial_tag()
            if cache.hexists(tag, options):
                data = json.loads(cache.hget(tag, options))
            else:
                data = self.get_list()
                cache.hset(Commercial.get_commercial_tag(), options, json.dumps(data))
        else:
            data = self.get_list()
        return data

    def get_list(self):
        data = []
        commercials = Commercial.objects.filter(status=Commercial.STATUS_ACTIVE)
        for commercial in commercials:
            data.append({
                'id': commercial.id,
                'name':  commercial.name,
                'dates': self.get_details(commercial)
            })
        return data

    def get_details(self, commercial):
        data = []
        for detail in commercial.commercial_date_detail_set.all():
            data.append({
                'id': detail.id,
                'date': detail.date.strftime('%d/%m/%Y')
            })
        return data

    def get_context_data(self, **kwargs):
        data = {}
        commercials = self.get_queryset()
        data['commercial'] = [item for item in commercials]
        return data


class CommercialCreateDataJson(LoginRequiredMixin, PermissionRequiredMixin,
                               JSONResponseMixin, View):
    permissions = {
        "permission": ('sp.add_commercial', ),
    }
    SAVE_SUCCESSFUL = 'Comercial registrado'
    SAVE_ERROR = 'Ocurrio un error al registrar el comercial'


    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(CommercialCreateDataJson, self).dispatch(request, *args, **kwargs)

    def save_commercial(self, data):
        try:
            commercial = Commercial()
            commercial.name = data.get('name')
            commercial.brand = Brand.objects.get(pk=data.get('brand'))
            commercial.save()
            if settings.APPLICATION_CACHE:
                clean_cache = CleanCache()
                clean_cache.set_cache_result_tag(Commercial.get_commercial_tag())
                clean_cache.set_model(Commercial)
                clean_cache.update_cache_by_id([commercial.id], CleanCache.MODE_INSERT)
            return commercial, self.SAVE_SUCCESSFUL
        except Exception, e:
            return None, self.SAVE_ERROR

    def get_details(self, commercial):
        data = []
        for detail in commercial.commercial_date_detail_set.all():
            data.append({
                'id': detail.id,
                'date': detail.date.strftime('%d/%m/%Y')
            })
        return data

    def post(self, request, *args, **kwargs):
        context = {}
        data = json.loads(request.body)
        commercial, msg = self.save_commercial(data)
        context['status'] = 'success'
        context['message'] = msg
        if commercial is None:
            context['status'] = 'warning'
        else:
            context['result'] = {
                'name': commercial.name,
                'id': commercial.id,
                'dates':  self.get_details(commercial)
            }
        return self.render_to_response(context)