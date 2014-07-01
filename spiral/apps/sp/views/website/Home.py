# -*- coding: utf-8 -*-
import uuid
from django.shortcuts import redirect
from django.contrib import auth, messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import FormView, RedirectView, View
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from apps.sp.forms.User import LoginForm
from apps.common.email import Email


class HomeFormView(FormView):
    template_name = 'website/home.html'
    form_class = LoginForm

    def form_valid(self, form):
        data = form.clean()

        user = auth.authenticate(
            username=data.get('username', ''),
            password=data.get('password', '')
        )
        if user is not None and user.is_active:
            auth.login(self.request, user)
            return super(HomeFormView, self).form_valid(form)
        else:
            messages.error(self.request, _(u'Incorrect login or password.'))
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('dashboard_view'))
        return super(HomeFormView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('home')


class RegisterUser(View):
    USER_SAVE = 'Registro completado'
    ERROR_USER_SAVE = 'ocurrio un error al tratar de registrarlo'
    WARNING_USER_EMAIL = 'El correo utilizado ya se encuentra registrado'
    WARNING_USER_USERMANE = 'El username utilizado ya se encuentra registrado'


    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(RegisterUser, self).dispatch(request, *args, **kwargs)

    def save_user(self, data):
        try:

            if User.objects.filter(email=data.get('email')).exists():
                return None, self.WARNING_USER_EMAIL
            if User.objects.filter(username=data.get('username')).exists():
                return None, self.WARNING_USER_USERMANE
            user = User()
            user.username = data.get('username')
            user.set_password(data.get('password'))
            user.email = data.get('email')
            user.is_active = False
            user.save()
            return user, self.USER_SAVE
        except Exception,e:
            return None, self.ERROR_USER_SAVE

    def post(self, request, *args, **kwargs):
        data = request.POST
        user, msg = self.save_user(data)
        if user:
            return redirect(reverse('home'))
        else:
            messages.error(self.request, msg)
            return redirect(reverse('home'))


class RecoverPasswordFormView(View):
    SEND_RECOVER = 'su contrasseña ha sido enviada a su correo'
    ERROR_SEND = 'ocurrio un error al tratar de restaurar su contraseña'
    ERROR_EMAIL = 'Correo electronico invalido'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(RecoverPasswordFormView, self).dispatch(request, *args, **kwargs)

    def recover_password(self, data):
        try:
            user = User.objects.get(email=data.get('email'))
            password = uuid.uuid4().hex
            user.set_password(password)
            user.save()
            self.send_email(user, password)
            return user, self.SEND_RECOVER
        except Exception, e:
            return None, self.ERROR_EMAIL

    def send_email(self, user, password):
        data = {
            'template_name': 'helpers/email/recover_password.html',
            'subject': 'Spiral Producciones - Password!',
            'to': [user.email],
            'context': {
                'user': user,
                'password': password
            }
        }
        Email.send_html_email(**data)

    def post(self, request, *args, **kwargs):
        data = request.POST
        user, msg = self.recover_password(data)
        if user:
            messages.success(self.request, _(u'Contraseña enviado a su correo'))
            return redirect(reverse('home'))


class LoginAuthView(FormView):
    template_name = 'website/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        data = form.clean()

        user = auth.authenticate(
            username=data.get('username', ''),
            password=data.get('password', '')
        )
        if user is not None and user.is_active:
            auth.login(self.request, user)
            return super(LoginAuthView, self).form_valid(form)
        else:
            messages.error(self.request, _(u'Incorrect login or password.'))
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('home'))

        return super(LoginAuthView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('home')


class LogoutView(RedirectView):

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return reverse('home')