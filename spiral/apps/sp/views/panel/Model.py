# -*- coding: utf-8 -*-

from apps.common.view import SearchFormMixin
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, UpdateView,\
    DeleteView, ListView
from django.conf import settings
from apps.sp.models.Entry import Entry
from apps.common.view import LoginRequiredMixin


class ModelControlListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = 'panel/model/list.html'
    context_object_name = 'model_list'
    paginate_by = settings.PANEL_PAGE_SIZE