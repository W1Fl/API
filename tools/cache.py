import pickle
import uwsgi


class Cache:
    '''
    缓存类
    可以像字典一样调用
    可以设置保质期
    '''

    def __init__(self, cachename):
        self.cachename = cachename
        self._keys = set()

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        self.set(key, value)

    def clean(self):
        uwsgi.cache_clean(self.cachename)

    def del_(self, key):
        uwsgi.cache_del(key, self.cachename)
        self._keys.discard(key)

    def keys(self):
        return self._keys

    def get(self, item, default=None):
        item = str(item)
        if uwsgi.cache_exists(item, self.cachename):
            return pickle.loads(uwsgi.cache_get(item, self.cachename))
        else:
            return default

    def set(self, key, value, expires=0):
        key = str(key)
        value = pickle.dumps(value)
        if uwsgi.cache_exists(key, self.cachename):
            uwsgi.cache_update(key, value, expires, self.cachename)
        else:
            uwsgi.cache_set(key, value, expires, self.cachename)
        self._keys.add(key)
