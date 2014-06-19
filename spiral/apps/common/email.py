# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.core.mail import EmailMessage, get_connection, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings


class Email():

    @staticmethod
    def send_html_email(*args, **kwargs):
        try:
            from_email = kwargs.get('from_email', settings.EMAIL_HOST_USER)
            context = Context(kwargs.get('context'))
            template = get_template(kwargs.get('template_name'))
            body = template.render(context)
            subject = kwargs.get('subject')
            message = EmailMultiAlternatives(subject, '', from_email, kwargs.get('to'))
            message.attach_alternative(body, 'text/html')
            message.send(fail_silently=True)

        except Exception,e:
            pass
