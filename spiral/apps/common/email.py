# -*- coding: utf-8 -*-
from celery.task import task
from django.core.mail import EmailMessage, get_connection, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings


class Email():

    @staticmethod
    def get_html_email_message(*args, **kwargs):
        context = Context(kwargs.get('context', {}))
        template = get_template(kwargs.get('template_name'))
        html_content = template.render(context)
        from_email = kwargs.get('from_email', settings.DEFAULT_FROM_EMAIL)
        message = EmailMultiAlternatives(
            kwargs.get('subject', ''), kwargs.get('body', ''), from_email, kwargs.get('to', []))
        message.attach_alternative(html_content, 'text/html')
        return message
