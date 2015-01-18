# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from apps.common.view import SearchFormMixin
from apps.sp.forms.MediaFeature import MediaFeatureForm, MediaFeatureFiltersForm
from apps.sp.forms.MediaFeature import MediaFeatureValueForm, MediaFeatureValueFiltersForm
from apps.sp.models.PictureDetail import MediaFeature, MediaFeatureValue
from apps.common.view import LoginRequiredMixin, PermissionRequiredMixin


class MediaFeatureListView(LoginRequiredMixin, PermissionRequiredMixin,
                           SearchFormMixin, ListView):
    model = MediaFeature
    template_name = 'panel/media_feature/list.html'
    search_form_class = MediaFeatureFiltersForm
    paginate_by = settings.PANEL_PAGE_SIZE
    filtering = {
        'name': SearchFormMixin.ALL,
    }

    def get_context_data(self, **kwargs):
        context = super(MediaFeatureListView, self).get_context_data(**kwargs)
        context['menu'] = 'maintenance'
        return context


class MediaFeatureCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    model = MediaFeature
    form_class = MediaFeatureForm
    template_name = 'panel/media_feature/create.html'
    success_url = 'brand_list'
    permissions = {
        "permission": ('sp.add_mediafeature', ),
        }

    def get_context_data(self, **kwargs):
        context = super(MediaFeatureCreateView,self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('media_feature_list')


class MediaFeatureUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    model = MediaFeature
    form_class = MediaFeatureForm
    template_name = 'panel/media_feature/update.html'
    success_url = 'brand_list'
    permissions = {
        "permission": ('sp.change_mediafeature', ),
    }

    def get_context_data(self, **kwargs):
        context = super(MediaFeatureUpdateView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('media_feature_list')


class MediaFeatureDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    model = MediaFeature
    template_name = 'panel/media_feature/delete.html'
    success_url = 'brand_list'
    permissions = {
        "permission": ('sp.delete_mediafeature', ),
    }

    def get_context_data(self, **kwargs):
        context = super(MediaFeatureDeleteView,self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('media_feature_list')

#Otro


class MediaFeatureValueListView(LoginRequiredMixin, PermissionRequiredMixin,
                                SearchFormMixin, ListView):
    model = MediaFeatureValue
    template_name = 'panel/media_feature/values/list.html'
    search_form_class = MediaFeatureValueFiltersForm
    paginate_by = settings.PANEL_PAGE_SIZE
    filtering = {
        'name': SearchFormMixin.ALL,
    }

    def dispatch(self, request, *args, **kwargs):
        self.media_feature = MediaFeature.objects.get(pk=self.kwargs.get('pk'))
        return super(MediaFeatureValueListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(MediaFeatureValueListView, self).get_queryset()
        qs = qs.filter(media_feature=self.media_feature)
        return qs

    def get_context_data(self, **kwargs):
        context = super(MediaFeatureValueListView, self).get_context_data(**kwargs)
        context['menu'] = 'maintenance'
        context['media_feature'] = self.media_feature
        return context


class MediaFeatureValueCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    model = MediaFeatureValue
    form_class = MediaFeatureValueForm
    template_name = 'panel/media_feature/values/create.html'
    success_url = 'brand_list'
    permissions = {
        "permission": ('sp.add_mediafeaturevalue', ),
    }

    def get_form(self, form_class):
        media_feature = MediaFeature.objects.get(pk=self.kwargs.get('pk'))
        form = super(MediaFeatureValueCreateView, self).get_form(form_class)
        if self.request.POST.get('media_feature') is None:
            form.set_media_feature(media_feature)
        return form

    def get_context_data(self, **kwargs):
        context = super(MediaFeatureValueCreateView,self).get_context_data(**kwargs)
        context['media_feature'] = MediaFeature.objects.get(pk=self.kwargs.get('pk'))
        return context

    def get_success_url(self):
        return reverse('media_feature_value_list', kwargs={'pk': self.object.media_feature.id})


class MediaFeatureValueUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    model = MediaFeatureValue
    form_class = MediaFeatureValueForm
    template_name = 'panel/media_feature/values/update.html'
    success_url = 'brand_list'
    permissions = {
        "permission": ('sp.change_mediafeaturevalue', ),
    }

    def get_context_data(self, **kwargs):
        context = super(MediaFeatureValueUpdateView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('media_feature_value_list', kwargs={'pk': self.object.media_feature.id})


class MediaFeatureValueDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    model = MediaFeatureValue
    template_name = 'panel/media_feature/values/delete.html'
    success_url = 'brand_list'
    permissions = {
        "permission": ('sp.delete_mediafeaturevalue', ),
    }

    def get_context_data(self, **kwargs):
        context = super(MediaFeatureValueDeleteView,self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('media_feature_value_list', kwargs={'pk': self.object.media_feature.id})