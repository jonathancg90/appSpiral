# -*- coding: utf-8 -*-

from django.views.generic import ListView, RedirectView
from apps.sp.models.ModelHasCommercial import ModelHasCommercial
from apps.sp.models.Model import Model


class ModelHasCommercialListView(ListView):
    template_name = 'panel/model_has_commercial/list.html'
    model = ModelHasCommercial
    context_object_name = 'model_has_commercial'


    def get(self, request, *args, **kwargs):
        model_code = self.kwargs.get('key')
        try:
            self.model = Model.objects.get(model_code=model_code)
        except:
            self.model = Model(
                model_code = model_code
            )
            self.model.save()

        return super(ModelHasCommercialListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        qs = ModelHasCommercial.objects.filter(model=self.model)
        return qs

    def get_context_data(self, **kwargs):
        context = super(ModelHasCommercialListView, self).get_context_data(**kwargs)
        context['model'] = self.model
        return context


class ModelHasCommercialAddListView(ListView):
    template_name = 'panel/model_has_commercial/add_commercial.html'
    model = ModelHasCommercial

    def get_queryset(self):
        qs = super(ModelHasCommercialAddListView, self).get_queryset()
        return qs


class ModelHasCommercialDelRedirectView(RedirectView):

    def get_redirect_url(self, **kwargs):
        pass