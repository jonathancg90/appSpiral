# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.contrib import auth, messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import FormView, RedirectView, View
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, BadHeaderError
from django.core.mail import EmailMessage

from apps.sp.forms.User import LoginForm


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

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(RegisterUser, self).dispatch(request, *args, **kwargs)

    def save_user(self, data):
        try:
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
            self.send_email('prueba', 'mensaje', 'app@spiral.com.pe')
            return user, self.SEND_RECOVER
        except Exception, e:
            return None, self.ERROR_EMAIL

    def send_email(self, subject, message, from_email):
        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email, ['jonathancg90@gmail.com'])
            except BadHeaderError:
                messages.error(self.request, _(u'Ocurrio un error al enviar el correo.'))
                return redirect(reverse('home'))
            except Exception, e:
                messages.error(self.request, _(u'No se ha podido restaurar su contraseña, consulte con soporte.'))
                return redirect(reverse('home'))
        else:
            messages.error(self.request, _(u'Parametros invalidos, para restaurar su contraseña.'))
            return redirect(reverse('home'))

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