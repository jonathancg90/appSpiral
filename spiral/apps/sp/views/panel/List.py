# -*- coding: utf-8 -*-
import json

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import TemplateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import FormView
from django.views.generic import View
from django.views.generic import RedirectView

from apps.common.view import SearchFormMixin
from apps.common.view import JSONResponseMixin

from apps.sp.models.Model import Model
from apps.sp.models.UserProfile import UserProfile
from apps.sp.forms.List import ListForm, ListFiltersForm, CollaborationForm
from apps.sp.models.List import List, UserCollaborationDetail, DetailList
from apps.common.view import LoginRequiredMixin, PermissionRequiredMixin


class ListListView(LoginRequiredMixin, PermissionRequiredMixin,
                    SearchFormMixin, ListView):
    model = UserCollaborationDetail
    template_name = 'panel/list/list.html'
    search_form_class = ListFiltersForm
    paginate_by = settings.PANEL_PAGE_SIZE
    filtering = {
        'title': SearchFormMixin.ALL,
    }

    def get_queryset(self):
        qs = super(ListListView, self).get_queryset()
        user_collaboration = qs.filter(
            user=self.request.user,
            is_owner=True,
            list__status=List.STATUS_ACTIVE
        )
        user_collaboration = user_collaboration.prefetch_related('list')
        return user_collaboration

    def get_list_collaboration(self):
        collaboration = UserCollaborationDetail.objects.filter(user=self.request.user)
        collaboration = collaboration.filter(list__status=List.STATUS_ACTIVE)
        collaboration = collaboration.filter(is_owner=False)
        return collaboration

    def get_list_archives(self):
        collaboration = UserCollaborationDetail.objects.filter(user=self.request.user)
        collaboration = collaboration.filter(list__status=List.STATUS_ARCHIVE)
        collaboration = collaboration.filter(is_owner=True)
        return collaboration

    def get_context_data(self, **kwargs):
        context = super(ListListView, self).get_context_data(**kwargs)
        context['menu'] = 'list'
        context['collaboration'] = self.get_list_collaboration()
        context['archives'] = self.get_list_archives()
        return context


class ListCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    model = List
    form_class = ListForm
    template_name = 'panel/list/create.html'
    success_url = 'list_list'
    permissions = {
        "permission": ('sp.add_list', ),
    }

    def get_form(self, form_class):
        form = super(ListCreateView, self).get_form(form_class)
        cod_emp = None
        if not self.request.user.is_superuser:
            cod_emp = UserProfile.objects.get(user=self.request.user).cod_emp
        form.set_project(cod_emp)
        return form

    def form_valid(self, form):
        list = form.save()
        user_collaboration = UserCollaborationDetail()
        user_collaboration.user = self.request.user
        user_collaboration.list = list
        user_collaboration.is_owner = True
        user_collaboration.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ListCreateView,self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('list_list')


class ListUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    model = List
    form_class = ListForm
    template_name = 'panel/list/update.html'
    success_url = 'list_list'
    permissions = {
        "permission": ('sp.change_list', ),
    }

    def get_context_data(self, **kwargs):
        context = super(ListUpdateView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('list_list')


class ListDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    model = List
    template_name = 'panel/list/delete.html'
    permissions = {
        "permission": ('sp.delete_list', ),
    }

    def get_context_data(self, **kwargs):
        context = super(ListDeleteView,self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('list_list')


class DetailListCollaborationView(LoginRequiredMixin,PermissionRequiredMixin, FormView):
    model = UserCollaborationDetail
    template_name = 'panel/list/detail.html'
    form_class = CollaborationForm

    def get_users_collaboration(self):
        return UserCollaborationDetail.objects.filter(
            list_id=self.kwargs["pk"]
        ).exclude(user=self.request.user)

    def get_form(self, form_class):
        form = super(DetailListCollaborationView, self).get_form(form_class)
        users = []
        for collaboration in self.get_users_collaboration():
            users.append(collaboration.user.id)
        users.append(self.request.user.pk)
        form.set_users(users)
        return form

    def form_valid(self, form):
        collaboration = UserCollaborationDetail()
        collaboration.user = form.cleaned_data["user"]
        collaboration.list = List.objects.get(pk=self.kwargs["pk"])
        collaboration.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(DetailListCollaborationView,self).get_context_data(**kwargs)
        context['list'] = List.objects.get(pk=self.kwargs.get('pk'))
        context['user_collaboration'] = self.get_users_collaboration()
        return context

    def get_success_url(self):
        return reverse('list_collaboration', kwargs={'pk': self.kwargs["pk"]})


class UserCollaborationDelete(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        user_collaboration = UserCollaborationDetail.objects.get(id=self.kwargs.get('pk'))
        user_collaboration.delete()
        return reverse('list_collaboration', kwargs={'pk': self.kwargs.get('list_fk')})


class UserListArchived(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        list = List.objects.get(id=self.kwargs.get('pk'))
        list.status = List.STATUS_ARCHIVE
        list.save()
        return reverse('list_list')


class UserListActive(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        list = List.objects.get(id=self.kwargs.get('pk'))
        list.status = List.STATUS_ACTIVE
        list.save()
        return reverse('list_list')


class ListDataListView(LoginRequiredMixin, PermissionRequiredMixin,
                             JSONResponseMixin, ListView):
    model = UserCollaborationDetail

    def get_queryset(self):
        data = []
        user_collaborations = UserCollaborationDetail.objects.filter(user=self.request.user)
        user_collaborations = user_collaborations.prefetch_related('list')
        user_collaborations = user_collaborations.exclude(list__status=List.STATUS_ARCHIVE)
        for user_collaboration in user_collaborations:
            data.append({
                'id': user_collaboration.list.id,
                'name': user_collaboration.list.title
            })
        return data

    def get_context_data(self, **kwargs):
        data = {}
        data['list'] = self.get_queryset()
        return data


class ListDataSaveView(LoginRequiredMixin, PermissionRequiredMixin,
                        JSONResponseMixin, View):
    permissions = {
        "permission": ('sp.add_list', ),
    }
    SAVE_SUCCESSFUL = 'Lista registrado'
    SAVE_ERROR = 'Ocurrio un error al registrar la lista'


    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(ListDataSaveView, self).dispatch(request, *args, **kwargs)

    def save_list(self, data):
        try:
            list = List()
            list.title = data.get('title')
            list.save()

            user_collaboration = UserCollaborationDetail()
            user_collaboration.list = list
            user_collaboration.user = self.request.user
            user_collaboration.is_owner = True
            user_collaboration.save()

            return list, self.SAVE_SUCCESSFUL
        except Exception, e:
            return None, self.SAVE_ERROR

    def post(self, request, *args, **kwargs):
        context = {}
        data = json.loads(request.body)
        list, msg = self.save_list(data)
        context['status'] = 'success'
        context['message'] = msg
        if list is None:
            context['status'] = 'warning'
        else:
            context['result'] = {
                'name': list.title,
                'id': list.id,
            }
        return self.render_to_response(context)


class ListAddModelView(LoginRequiredMixin, PermissionRequiredMixin,
                       JSONResponseMixin, View):
    permissions = {
        "permission": ('sp.add_list', ),
    }
    SAVE_SUCCESSFUL = 'Se agrego a tu lista'
    SAVE_ERROR = 'Ocurrio un error al agregar al modelo en la lista'
    WARNING_ADD = 'El modelo ya se encuentra en la lista'


    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(ListAddModelView, self).dispatch(request, *args, **kwargs)

    def save_list(self, data):
        try:

            if DetailList.objects.filter(
                list_id=data.get('list_id'),
                model_id=data.get('model_id')
            ).exists():
                return None, self.WARNING_ADD

            detail_list = DetailList()
            detail_list.model = Model.objects.get(pk=data.get('model_id'))
            detail_list.list = List.objects.get(pk=data.get('list_id'))
            detail_list.save()

            return detail_list, self.SAVE_SUCCESSFUL
        except Exception, e:
            return None, self.SAVE_ERROR

    def post(self, request, *args, **kwargs):
        context = {}
        data = json.loads(request.body)
        detail, msg = self.save_list(data)
        context['status'] = 'success'
        context['message'] = msg
        if detail is None:
            context['status'] = 'warning'
        return self.render_to_response(context)


class ListModelView(LoginRequiredMixin, PermissionRequiredMixin,
                    JSONResponseMixin, View):
    model = DetailList

    def get_data_model(self, detail):
        if detail.model is None:
            return {
                'photo': Model.DEFAULT_IMAGE,
                'name_complete': detail.name_complete,
                'dni': detail.DNI,
                'phone': detail.phone,
                'model_code': False
            }
        else:
            return {
                'model_code': detail.model.model_code,
                'photo': detail.model.main_image,
                'measures': 'Altura: %s %s' %(detail.model.height,'' if detail.model.weight is None else ' - peso: '+detail.model.weight),
                'name_complete': detail.model.name_complete,
                'dni': detail.model.number_doc,
                'phone': '%s | %s' %(detail.model.phone_fixed, detail.model.phone_mobil)
            }

    def get_models_list(self, id_list):
        data = []
        detail_list = DetailList.objects.filter(list_id=id_list)
        for detail in detail_list:
            model = self.get_data_model(detail)
            data.append({
                'id': detail.id,
                'model': model,
                'observation': detail.observation,
                'url': reverse('list_detail_delete', kwargs={'pk': detail.id })
            })
        return data

    def get(self, request, *args, **kwargs):
        context = {}
        id_list = kwargs.get('pk')
        context['models'] = self.get_models_list(id_list)
        return self.render_to_response(context)


class ListDetailView(LoginRequiredMixin, PermissionRequiredMixin,
                     TemplateView):
    template_name = 'panel/list/models.html'
    model = DetailList

    def get_context_data(self, **kwargs):
        context = super(ListDetailView, self).get_context_data(**kwargs)
        context['list'] = List.objects.get(pk=kwargs.get('pk'))
        return context


class ListDetailDelete(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, **kwargs):
        list_detail = DetailList.objects.get(pk=kwargs.get('pk'))
        list = list_detail.list
        list_detail.delete()
        return reverse('list_detail', kwargs={'pk': list.id})


class ListDetailModelSaveView(LoginRequiredMixin, PermissionRequiredMixin,
                       JSONResponseMixin, View):
    model = DetailList
    SAVE_SUCCESSFUL = 'Se agrego el modelo a tu lista'
    SAVE_ERROR = 'Ocurrio un error al agregar al modelo en la lista'
    WARNING_ADD = 'El modelo ya se encuentra en la lista'


    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(ListDetailModelSaveView, self).dispatch(request, *args, **kwargs)

    def save_detail_list(self, data):
        try:
            detail_list = DetailList()
            detail_list.list = List.objects.get(pk=self.kwargs.get('pk'))
            detail_list.name_complete = data.get('model').get('name_complete')
            detail_list.DNI = data.get('model').get('dni')
            detail_list.phone = data.get('model').get('phone')
            detail_list.observation = data.get('observation')
            detail_list.save()
            return detail_list, self.SAVE_SUCCESSFUL
        except Exception, e:
            return None, self.SAVE_ERROR

    def post(self, request, *args, **kwargs):
        context = {}
        data = json.loads(request.body)
        detail, msg = self.save_detail_list(data)
        context['status'] = 'success'
        context['message'] = msg
        if detail is None:
            context['status'] = 'warning'
        else:
            context['model'] = {
                'id': detail.id,
                'model': {
                    'photo': Model.DEFAULT_IMAGE,
                    'name_complete': detail.name_complete,
                    'dni': detail.DNI,
                    'phone': detail.phone,
                    'model_code': False
                },
                'observation': detail.observation,
                'url': reverse('list_detail_delete', kwargs={'pk': detail.id })
            }
        return self.render_to_response(context)


class ListDetailModelUpdateView(LoginRequiredMixin, PermissionRequiredMixin,
                              JSONResponseMixin, View):
    model = DetailList
    SAVE_SUCCESSFUL = 'Se actualizo modelo'
    SAVE_ERROR = 'Ocurrio un error al agregar al modelo en la lista'
    WARNING_ADD = 'El modelo ya se encuentra en la lista'


    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(ListDetailModelUpdateView, self).dispatch(request, *args, **kwargs)

    def update_detail_list(self, data):
        try:
            detail_list = DetailList.objects.get(pk=data.get('id'))
            detail_list.name_complete = data.get('model').get('name_complete')
            detail_list.DNI = data.get('model').get('dni')
            detail_list.phone = data.get('model').get('phone')
            detail_list.observation = data.get('observation')
            detail_list.save()
            return detail_list, self.SAVE_SUCCESSFUL
        except Exception, e:
            return None, self.SAVE_ERROR

    def post(self, request, *args, **kwargs):
        context = {}
        data = json.loads(request.body)
        detail, msg = self.update_detail_list(data)
        context['status'] = 'success'
        context['message'] = msg
        if detail is None:
            context['status'] = 'warning'
        else:
            context['model'] = {
                'id': detail.id,
                'model': {
                    'photo': Model.DEFAULT_IMAGE,
                    'name_complete': detail.name_complete,
                    'dni': detail.DNI,
                    'phone': detail.phone,
                    'model_code': False
                },
                'observation': detail.observation,
                'url': reverse('list_detail_delete', kwargs={'pk': detail.id })
            }
        return self.render_to_response(context)