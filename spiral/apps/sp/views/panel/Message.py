# -*- coding: utf-8 -*-

import json

from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import View

from apps.common.email import Email
from apps.common.view import LoginRequiredMixin, PermissionRequiredMixin
from apps.common.view import SearchFormMixin
from apps.common.view import JSONResponseMixin

from apps.sp.forms.Message import MessageForm, MessageFiltersForm
from apps.sp.models.Message import Message
from apps.sp.models.Model import Model


class MessageListView(LoginRequiredMixin, PermissionRequiredMixin,
                      SearchFormMixin, ListView):
    model = Message
    template_name = 'panel/message/list.html'
    search_form_class = MessageFiltersForm
    paginate_by = settings.PANEL_PAGE_SIZE
    filtering = {
        'name': SearchFormMixin.ALL,
    }

    def get_queryset(self):
        qs = super(MessageListView, self).get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super(MessageListView, self).get_context_data(**kwargs)
        return context


class MessageCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'panel/message/create.html'
    permissions = {
        "permission": ('sp.add_message', ),
    }

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        return super(MessageCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('message_list')


class MessageUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'panel/message/update.html'
    permissions = {
        "permission": ('sp.change_message', ),
    }

    def get_success_url(self):
        return reverse('message_list')


class MessageDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    model = Message
    template_name = 'panel/message/delete.html'
    permissions = {
        "permission": ('sp.delete_message', ),
    }

    def get_success_url(self):
        return reverse('message_list')


class MessageListJsonView(LoginRequiredMixin, PermissionRequiredMixin,
                          JSONResponseMixin, View):
    model = Message

    def get_messages(self):
        data = []
        messages = Message.objects.filter(user=self.request.user)
        for message in messages:
            data.append({
                'id': message.id,
                'name': message.name

            })
        return data

    def get(self, request, *args, **kwargs):
        context = {}
        context['message'] = self.get_messages()
        return self.render_to_response(context)


class SendMessageJsonView(LoginRequiredMixin, PermissionRequiredMixin,
                          JSONResponseMixin, View):
    model = Message

    def get_attributes(self, data):
        self.model_id = data.get('model').get('id')
        self.message_id = data.get('message').get('id')

    def get_messages(self):
        data = []
        email = Model.objects.get(id=self.model_id).email
        if Model.objects.get(id=self.model_id).email is not None:
            message = Message.objects.get(pk=self.message_id)
            data = {
                'template_name': 'email/invitation/search.html',
                'subject': str(message.subject),
                'from_email': self.request.user.email,
                'to': [email],
                'context': {
                    'message': message.content
                }
            }
            message = Email.get_html_email_message(**data)
            message.content_subtype = "html"
            message.send(fail_silently=True)
        return data

    def post(self, request, *args, **kwargs):
        context = {}
        data = json.loads(request.body)
        self.get_attributes(data)
        context['message'] = self.get_messages()
        return self.render_to_response(context)

