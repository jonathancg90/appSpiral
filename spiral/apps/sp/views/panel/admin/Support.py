# -*- coding: utf-8 -*-
from django.conf import settings
from django.views.generic import ListView
from django.core.urlresolvers import reverse
from django.views.generic import RedirectView, View
from django.views.decorators.csrf import csrf_exempt

from apps.sp.models.Support import Support
from apps.common.view import JSONResponseMixin
from apps.common.view import LoginRequiredMixin, PermissionRequiredMixin


class AdminSupportListView(LoginRequiredMixin, ListView):
    template_name = 'panel/admin/support/list.html'
    model = Support
    paginate_by = settings.PANEL_PAGE_SIZE

    def get_queryset(self):
        qs = super(AdminSupportListView, self).get_queryset()
        qs = qs.filter(status=Support.STATUS_ACTIVE)
        return qs


class AdminSupportReportView(LoginRequiredMixin, PermissionRequiredMixin,
                             JSONResponseMixin, View):
    template_name = 'panel/admin/support/list.html'
    model = Support
    permissions = {
        "permission": ('sp.add_support', ),
    }

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(AdminSupportReportView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context = {}
        context['status'] = 'success'
        context['message'] = 'Su mensaje ha sido enviado'

        text = request.POST.get('text', None)
        if text is not None:
            support = Support()
            support.user = self.request.user
            support.text = text
            support.save()
        else:
            context['status'] = 'warning'
            context['message'] = 'No se pudo registrar'

        return self.render_to_response(context)


class AdminSupportCompleteRedirectView(LoginRequiredMixin,
                                       PermissionRequiredMixin,
                                       RedirectView):
    permanent = False
    permissions = {
        "permission": ('sp.change_support', ),
    }

    def get_redirect_url(self, **kwargs):
        support = Support.objects.get(pk=kwargs.get('pk'))
        support.status = Support.STATUS_INACTIVE
        support.save()
        return reverse('admin_user_support_list')