from django.views.generic import ListView, RedirectView
from apps.sp.models.ModelHasCommercial import ModelHasCommercial
from apps.sp.models.Model import Model


class ModelHasCommercialListView(ListView):
    template_name = 'panel/model_has_commercial/list.html'
    model = ModelHasCommercial
    context_object_name = 'model_has_commercial'


    def get(self, request, *args, **kwargs):
        model_code =  self.kwargs.get('key')
        try:
            self.model = Model.objects.get(model_code=model_code)
        except:
            model = Model(
                model_code = model_code
            )
            self.model.save()


        return super(ModelHasCommercialListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(ModelHasCommercialListView, self).get_queryset()
        qs = qs.filter()
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