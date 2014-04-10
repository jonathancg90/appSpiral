# -*- coding: utf-8 -*-
from django.views.generic import View, ListView
from apps.common.view import JSONResponseMixin
from apps.sp.models.Project import Project
import poplib
from email import parser


class EmailListView(JSONResponseMixin, ListView):
    model = Project
    template_name = 'website/email.html'

    def get_queryset(self):
        return None

    def get_emails(self):
        data = []
        pop_conn = poplib.POP3_SSL('pop.gmail.com')
        pop_conn.user('jonathancg90@gmail.com')
        pop_conn.pass_('74295290*')
        #Get messages from server:
        messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
        # Concat message pieces:
        messages = ["\n".join(mssg[1]) for mssg in messages]
        #Parse message intom an email object:
        messages = [parser.Parser().parsestr(mssg) for mssg in messages]
        for message in messages:
            data.append({
                'asunto': str(message['subject'])
            })
        pop_conn.quit()
        return data

    def get_context_data(self, **kwargs):
        data = {}
        data['emails'] = self.get_emails()
        return data