import urllib
import requests
from behance_python import ENDPOINTS, url_join
from exceptions import BehanceException
from requests.exceptions import ConnectionError, HTTPError, Timeout, TooManyRedirects

#   TODO: Very similar to Project class. Refactor and inherit common class.
#   TODO: Should get_projects return project objects? How to do this with min overhead?

class User:

    def __init__(self, user_id, auth_key):
        self.user_id = user_id
        self.auth_key = auth_key
        self.base_url = url_join(ENDPOINTS['api'], ENDPOINTS['user'])

        self._get_user_details()

    def _add_property(self, name, value):
        """Helper function to dynamically add all the JSON data from API response
        to the Project object."""
        setattr(self.__class__, name, value)

    def _get_api_data(self, url):
        """Internal helper to call API and handle exceptions"""
        try:
            _results = requests.get(url)

            #Parse the data
            if _results.status_code == 200:
                return _results.json
            else:
                #If error from API, raise exception
                raise BehanceException(_results.status_code)
        except (ConnectionError, HTTPError, Timeout, TooManyRedirects) as e:
            #If requests raises and exception
            raise e

    def _get_user_details(self):
        #Build the URL
        _url = url_join(self.base_url, str(self.user_id))
        _url = "%s?api_key=%s" % (_url, self.auth_key)

        #Call the API
        #_results = requests.get(_url)
        _results = self._get_api_data(_url)

        for k, v in _results.items():
            self._add_property(k, v)

    def get_projects(self, **kwargs):
        _base_url = url_join(self.base_url, self.user_id, 'projects')
        if len(kwargs) > 0:
            _filters = urllib.urlencode(kwargs)
            _url = '%s?api_key=%s&%s' % (_base_url, self.auth_key, _filters)
        else:
            _url = '%s?api_key=%s' % (_base_url, self.auth_key)

        return self._get_api_data(_url)['projects']

    def get_wips(self, **kwargs):
        _base_url = url_join(self.base_url, self.user_id, 'wips')
        if len(kwargs) > 0:
            _filters = urllib.urlencode(kwargs)
            _url = '%s?api_key=%s&%s' % (_base_url, self.auth_key, _filters)
        else:
            _url = '%s?api_key=%s' % (_base_url, self.auth_key)

        return self._get_api_data(_url)['wips']

    def get_appreciations(self, **kwargs):
        _base_url = url_join(self.base_url, self.user_id, 'appreciations')
        if len(kwargs) > 0:
            _filters = urllib.urlencode(kwargs)
            _url = '%s?api_key=%s&%s' % (_base_url, self.auth_key, _filters)
        else:
            _url = '%s?api_key=%s' % (_base_url, self.auth_key)

        return self._get_api_data(_url)['appreciations']

    def get_collections(self, **kwargs):
        _base_url = url_join(self.base_url, self.user_id, 'collections')
        if len(kwargs) > 0:
            _filters = urllib.urlencode(kwargs)
            _url = '%s?api_key=%s&%s' % (_base_url, self.auth_key, _filters)
        else:
            _url = '%s?api_key=%s' % (_base_url, self.auth_key)

        return self._get_api_data(_url)['collections']