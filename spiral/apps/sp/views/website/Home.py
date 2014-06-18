# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.contrib import auth, messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import FormView, RedirectView, View
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from apps.sp.forms.User import LoginForm, RecoverForm


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


class RecoverPasswordFormView(FormView):
    template_name = 'website/recover_password.html'
    form_class = RecoverForm

    def form_valid(self, form):
        data = form.clean()
        user = User.objects.get(pk=1)
        user.set_password(data.get('password'))
        user.save()
        return super(RecoverPasswordFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse('home')


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