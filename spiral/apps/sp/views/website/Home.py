from django.contrib import auth, messages
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, FormView, RedirectView
from apps.sp.forms.User import LoginForm
from django.utils.translation import ugettext_lazy as _


class HomeTemplateView(TemplateView):
    template_name = 'home.html'


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