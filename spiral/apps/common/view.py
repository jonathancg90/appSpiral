# -*- coding: utf-8 -*-
import json
from django import http
from .util import dict_strip_unicode_keys
from django.utils import simplejson
from django.http import HttpResponseBadRequest
from django.core.exceptions import ImproperlyConfigured
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.http import HttpResponse



class InvalidFilterError(Exception):
    pass


class SearchMixin(object):
    """
    Adds search functionality to a ListView
    """

    LOOKUP_SEP = '__'
    QUERY_TERMS = dict([(x, None) for x in (
        'exact', 'iexact', 'contains', 'icontains', 'gt', 'gte', 'lt', 'lte',
        'in',
        'startswith', 'istartswith', 'endswith', 'iendswith', 'range', 'year',
        'month', 'day', 'week_day', 'isnull', 'search', 'regex', 'iregex',
        )])

    # Enable all basic ORM filters but do not allow filtering across
    # relationships.
    ALL = 1
    # Enable all ORM filters, including across relationships
    ALL_WITH_RELATIONS = 2
    ignore_blank_parameters = True
    filtering = {}
    sort_parameter_name = 'order_by'

    def get_filtering(self):
        """
        Returns filtering list
        """
        return self.filtering

    def get_allowed_filter_fields(self):
        """
        Returns a list of fields that can be used as filters
        """
        return self.get_filtering().keys()

    def build_filters(self, filters=None):
        """
        Given a dictionary of filters, create the necessary ORM-level filters.

        Keys should be resource fields, **NOT** model fields.

        Valid values are either a list of Django filter types (i.e.
        ``['startswith', 'exact', 'lte']``), the ``ALL`` constant or the
        ``ALL_WITH_RELATIONS`` constant.
        """
        # At the declarative level:
        #     filtering = {
        #         'resource_field_name': ['exact', 'startswith', 'endswith', 'contains'],
        #         'resource_field_name_2': ['exact', 'gt', 'gte', 'lt', 'lte', 'range'],
        #         'resource_field_name_3': ALL,
        #         'resource_field_name_4': ALL_WITH_RELATIONS,
        #         ...
        #     }
        # Accepts the filters as a dict. None by default, meaning no filters.
        if filters is None:
            filters = {}

        qs_filters = {}

        for filter_expr, value in filters.items():
            filter_bits = filter_expr.split(self.LOOKUP_SEP)
            field_name = filter_bits.pop(0)
            filter_type = 'exact'

            if self.ignore_blank_parameters and (value is None or value == ''):
                continue

            if not field_name in self.get_allowed_filter_fields():
                # It's not a field we know about. Move along citizen.
                continue

            if len(filter_bits) and filter_bits[-1] in self.QUERY_TERMS.keys():
                filter_type = filter_bits.pop()

            lookup_bits = self.check_filtering(field_name, filter_type, filter_bits)

            if value in ['true', 'True', True]:
                value = True
            elif value in ['false', 'False', False]:
                value = False
            elif value in ('nil', 'none', 'None', None):
                value = None

            # Split on ',' if not empty string and either an in or range filter.
            if filter_type in ('in', 'range') and len(value):
                if hasattr(filters, 'getlist'):
                    value = filters.getlist(filter_expr)
                else:
                    value = value.split(',')

            db_field_name = self.LOOKUP_SEP.join(lookup_bits)
            qs_filter = "%s%s%s" % (db_field_name, self.LOOKUP_SEP, filter_type)
            qs_filters[qs_filter] = value

        return dict_strip_unicode_keys(qs_filters)

    def check_filtering(self, field_name, filter_type='exact', filter_bits=None):
        """
        Given a field name, a optional filter type and an optional list of
        additional relations, determine if a field can be filtered on.

        If a filter does not meet the needed conditions, it should raise an
        ``InvalidFilterError``.

        If the filter meets the conditions, a list of attribute names (not
        field names) will be returned.
        """

        filtering = self.get_filtering()
        fields = self.get_allowed_filter_fields()

        if filter_bits is None:
            filter_bits = []

        if not field_name in filtering:
            raise InvalidFilterError("The '%s' field does not allow filtering." % field_name)

        # Check to see if it's an allowed lookup type.
        if not filtering[field_name] in (self.ALL, self.ALL_WITH_RELATIONS):
            # Must be an explicit whitelist.
            if not filter_type in filtering[field_name]:
                raise InvalidFilterError("'%s' is not an allowed filter on the '%s' field." % (filter_type, field_name))

        return [field_name]


    def apply_sorting(self, queryset):
        """
        Given a dictionary of options, apply some ORM-level sorting to the
        provided ``QuerySet``.

        Looks for the ``order_by`` key and handles either ascending (just the
        field name) or descending (the field name with a ``-`` in front).

        The field name should be the resource field, **NOT** model field.
        """
        parameter_name = self.sort_parameter_name

        order_by_field = self.request.GET.get(parameter_name, None)
        if order_by_field:
            return queryset.order_by(order_by_field)

        return queryset


    def get_queryset(self):
        qs = super(SearchMixin, self).get_queryset()

        filters = {}
        if hasattr(self.request, 'GET'):
            # Grab a mutable copy.
            filters = self.request.GET.copy()

        applicable_filters = self.build_filters(filters=filters)
        qs = qs.filter(**applicable_filters)
        qs = self.apply_sorting(qs)

        return qs

    def get_context_data(self, **kwargs):
        context = super(SearchMixin, self).get_context_data(**kwargs)
        context['search_url_params'] = self.request.GET.copy()
        return context


class SearchFormMixin(SearchMixin):
    """

    """
    search_form_class = None
    search_initial = {}

    def get_search_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = self.search_initial.copy()
        return initial.update(self.request.GET.copy())

    def get_search_form_class(self):
        """
        Returns the form class to use in this view
        """
        return self.search_form_class

    def get_search_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        return form_class(**self.get_search_form_kwargs())

    def get_search_form_kwargs(self):
        """
        Returns the keyword arguments for instanciating the form.
        """
        kwargs = {'initial': self.get_search_initial()}
        if self.request.method in ('POST', 'GET'):
            kwargs.update({
                'data': self.request.GET
            })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(SearchFormMixin, self).get_context_data(**kwargs)

        # TODO :
        context.update({
            'search_form': self.get_search_form(self.get_search_form_class())
        })
        return context


class JSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
            content_type='application/json',
            **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.

        return simplejson.dumps(context)



class NewJSONResponseMixin(object):
    """
    A mixin that allows you to easily serialize simple data such as a dict or
    Django models.
    """
    content_type = "application/json"

    def get_response_content_type(self):
        if self.content_type is None:
            raise ImproperlyConfigured("%(cls)s is missing a content type. "
                                       "Define %(cls)s.content_type, or override "
                                       "%(cls)s.get_content_type()." % {
                                           "cls": self.__class__.__name__
                                       })
        return self.content_type

    def render_json_response(self, context_dict, status_code=None):
        """
        Limited serialization for shipping plain data. Do not use for models
        or other complex or custom objects.
        """
        json_context = json.dumps(context_dict, cls=DjangoJSONEncoder, ensure_ascii=False)
        response = HttpResponse(json_context, content_type=self.get_response_content_type())

        if status_code == 400:
            return HttpResponseBadRequest(response)
        else:
            return response

    def render_json_object_response(self, objects, **kwargs):
        """
        Serializes objects using Django's builtin JSON serializer. Additional
        kwargs can be used the same way for django.core.serializers.serialize.
        """
        json_data = serializers.serialize("json", objects, **kwargs)
        return HttpResponse(json_data, content_type=self.get_response_content_type())

class LoginRequiredMixin(object):
    pass
    # @method_decorator(login_required)
    # def dispatch(self, request, *args, **kwargs):
    #     self.request = request
    #
    #     if self.request.user.is_authenticated():
    #         return super(LoginRequiredMixin, self).dispatch(
    #                         self.request, *args, **kwargs)
    #     else:
    #         return super(LoginRequiredMixin, self).dispatch(
    #             request, *args, **kwargs)