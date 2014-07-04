from json import loads, dumps
from django.conf import settings
from django.core.cache import cache

from apps.sp.models.Commercial import Commercial


class CleanCache(object):
    CACHE_RESULT_TAG = None
    MODEL = None
    MODE_INSERT = 1
    MODE_UPDATE = 2
    MODE_DELETE = 3

    def __init__(self):
        super(CleanCache, self).__init__()
        self.search_results = None

    def set_cache_result(self):
        if settings.APPLICATION_CACHE  and self.CACHE_RESULT_TAG is not None:
            try:
                self.search_results = cache.hgetall(self.CACHE_RESULT_TAG)
            except Exception:
                # TODO: Log this
                # Error trying to get all the cache search
                pass

    def set_cache_result_tag(self, tag):
        self.CACHE_RESULT_TAG = tag

    def set_model(self, model):
        self.MODEL = model

    def update_cache_by_id(self, ids, mode):
        self.set_cache_result()

        if self.search_results is None:
            return
        if self.MODEL is None:
            return

        for id in ids:
            if mode == self.MODE_UPDATE:
                self.update_cache(id)
            if mode == self.MODE_INSERT:
                self.insert_cache(id)
            if mode == self.MODE_DELETE:
                self.delete_cache(id)

    def delete_cache(self, id):
        for key, result in self.search_results.iteritems():
            result = loads(result) if isinstance(result, str) else result
            new_result = []
            for item in result:
                if str(item.get('pk')) != str(id):
                    self.delete_result(key)
                    new_result.append(item)
            cache.hset(self.CACHE_RESULT_TAG, key, dumps(new_result))

    def update_cache(self, id):
        for key, result in self.search_results.iteritems():
            result = loads(result) if isinstance(result, str) else result
            new_result = []
            for item in result:
                if str(item.get('pk')) == str(id):
                    self.delete_result(key)
                    if self.MODEL == Commercial:
                        commercial = Commercial.objects.get(pk=item.get('pk'))
                        item = self.get_commercial_data(commercial)
                new_result.append(item)
            cache.hset(self.CACHE_RESULT_TAG, key, dumps(new_result))

    def insert_cache(self, id):
        for key, result in self.search_results.iteritems():
            result = loads(result) if isinstance(result, str) else result
            try:
                commercial = Commercial.objects.get(pk=id)
                self.delete_result(key)
                commercial = self.get_commercial_data(commercial)
                result.append(commercial)
                cache.hset(self.CACHE_RESULT_TAG, key, dumps(result))
            except:
                pass

    def delete_result(self, key):
        cache.hdel(self.CACHE_RESULT_TAG, key)

    def get_commercial_data(self, commercial):
        data = {
            'pk': commercial.id,
            'id': commercial.id,
            'name': commercial.name,
            'realized': commercial.realized,
            'project':  commercial.project,
            'brand': commercial.brand.name,
            'entry': commercial.brand.entry.name
        }
        return data

