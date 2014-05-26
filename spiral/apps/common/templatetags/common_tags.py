from classytags.core import Options
from classytags.arguments import Argument, KeywordArgument
from classytags.helpers import InclusionTag
from django import template
from django.db.models.loading import get_model
import urllib

register = template.Library()


class PaginationCtl(InclusionTag):
    name = 'pagination_ctl'
    template = 'templatetags/pagination_ctl.html'

    options = Options(
        Argument('page', required=True, resolve=True),
        KeywordArgument('url', default='', required=False, resolve=True),
        KeywordArgument('url_args', default={}, required=False, resolve=True)
    )

    def get_context(self, context, page, url='', url_args={}):
        url = url.get('url', '')
        page_obj = page

        url_params = url_args.get('url_args', {})
        if 'page' in url_params:
            del url_params['page']

        url_args = urllib.urlencode(url_params)

        pages = []
        paginator = page_obj.paginator
        max_pages = 9

        if paginator.num_pages < max_pages:
            pages = range(1, paginator.num_pages + 1)

        else:
            half = max_pages // 2
            page_start = int(page_obj.number - half)

            if (page_start + max_pages) > paginator.num_pages:
                page_start = paginator.num_pages - max_pages

            if page_start > 0:
                pages = range(page_start, page_start + max_pages + 1)

            else:
                pages = range(1, max_pages + 1)

        return {
            'page_obj': page_obj,
            'url': url,
            'url_params': url_args,
            'page_range': pages
        }

register.tag(PaginationCtl)
