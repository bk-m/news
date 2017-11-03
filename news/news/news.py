# -*- coding: utf-8 -*-

"""
Main module.

Powered by NewsAPI.org

Key: 175b17969f3141fbb2af57b2b61e669e
IDs:
    - ars-technica
    - der-tagesspiegel
    - die-zeit
    - hacker-news
    - spiegel-online
    - the-guardian-uk
    - the-new-york-times
    - the-verge
    - wired-de
"""

import util.news_logger
import logging
import requests

LOGGER = logging.getLogger('news')

class IllegalArgumentError(ValueError):
    pass


class News():
    _base_url = 'https://newsapi.org/v1/articles'
    _api_key = '175b17969f3141fbb2af57b2b61e669e'

    def __init__(self, source=None, sort='latest'):
        if not source:
            raise IllegalArgumentError('Must pass a source')

        avail_sorts = self._get_available_sorts()
        if sort not in avail_sorts[source]:
            LOGGER.debug('Chosen sorting not available')
            if len(avail_sorts[source]) > 0:
                sort = avail_sorts[source][0]
                LOGGER.debug('Setting sort to {}'.format(sort))
            else:
                sort = None
                LOGGER.debug('No sorting option found. Setting sort to None.')
        self.payload = {'source': source, 'sortBy': sort, 'apiKey': News._api_key}

    def get_news(self):
        return requests.get(News._base_url, params=self.payload).json()

    def _get_available_sorts(self):
        response = requests.get('https://newsapi.org/v1/sources').json()
        ret_val = {}
        if response['status'] == 'ok':
            ret_val = {source['id']: source['sortBysAvailable'] for source in response['sources']}
        else:
            LOGGER.error("Server error. Coudn't get available sorts.")
        return ret_val



def main():
    ids = ['hacker-news', 'spiegel-online']
    tmp = [News(val).get_news() for val in ids]

    for resp in tmp:
        print('Source: {}'.format(resp['source']))
        for article in resp['articles']:
            print(article['title'])
        print('-------------------------------------------------------------------------')

if __name__ == '__main__':
    main()
