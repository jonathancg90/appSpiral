from django.views.generic import ListView, RedirectView
from apps.sp.models.ModelHasCommercial import ModelHasCommercial


class ModelHasCommercialListView(ListView):
    template_name = 'panel/model_has_commercial/list.html'
    model = ModelHasCommercial
    context_object_name = 'model_has_commercial'

    def get_queryset(self):
        qs = super(ModelHasCommercialListView, self).get_queryset()
        return qs


class ModelHasCommercialAddListView(ListView):
    template_name = 'panel/model_has_commercial/add_commercial.html'
    model = ModelHasCommercial

    def get_queryset(self):
        qs = super(ModelHasCommercialListView, self).get_queryset()
        return qs


class ModelHasCommercialDelRedirectView(RedirectView):

    def get_redirect_url(self, **kwargs):
        pass