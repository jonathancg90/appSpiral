# -*- coding: utf-8 -*-

from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import View
from apps.sp.forms.Country import CountryForm
from apps.sp.models.Country import Country
from apps.sp.models.City import City
from apps.common.view import JSONResponseMixin
from apps.common.view import LoginRequiredMixin


class CountryCreateView(CreateView):
    form_class = CountryForm
    template = 'templates/CRUD.html'
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super(CountryCreateView,self).get_context_data(**kwargs)
        context['action'] = 'create'
        return context


class CountryUpdateView(UpdateView):
    form_class = CountryForm
    template = 'templates/CRUD.html'
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super(CountryUpdateView,self).get_context_data(**kwargs)
        context['action'] = 'update'
        return context


class CountryDeleteView(DeleteView):
    model = Country
    template = 'templates/CRUD.html'
    success_url = ''

    def get_context_data(self, **kwargs):
        context = super(CountryDeleteView,self).get_context_data(**kwargs)
        context['action'] = 'delete'
        return context


class CountryListView(ListView):
    model = Country
    template = ''


class CountryJsonView(JSONResponseMixin, View):

    def get_countries(self):
        data = []
        countries = Country.objects.all()
        for country in countries:
            data.append({
                'id': country.id,
                'name': country.name,
                'nationality': country.nationality,
                'cities': self.get_cities(country)
            })
        return data

    def get_cities(self, country):
        data = []
        cities = City.objects.filter(country=country)
        for city in cities:
            data.append({
                'city_id': city.id,
                'city_name': city.name
            })
        return data



    def get(self, request, *args, **kwargs):
        context = {}
        context['countries'] = self.get_countries()
        context['status'] = 200
        return self.render_to_response(context)