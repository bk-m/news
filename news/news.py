# -*- coding: utf-8 -*-

"""
Main module.

Powered by NewsAPI.org

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
import datetime
import requests
import yaml

LOGGER = logging.getLogger('news')

class IllegalArgumentError(ValueError):
    pass


class News():
    _base_url = 'https://newsapi.org/v1/articles'
    with open('data/keys.yml') as yml:
        _api_key = yaml.load(yml)['newsapi']

    def __init__(self, source=None, sort='latest'):
        if not source:
            raise IllegalArgumentError('Must pass a source.')

        avail_sorts = News._get_available_sorts()
        if sort not in avail_sorts[source]:
            LOGGER.debug('Chosen sorting not available.')
            if len(avail_sorts[source]) > 0:
                sort = avail_sorts[source][0]
                LOGGER.debug('Setting sort to {}.'.format(sort))
            else:
                sort = None
                LOGGER.debug('No sorting option found. Setting sort to None.')
        self.payload = {'source': source, 'sortBy': sort, 'apiKey': News._api_key}

    def get_news(self):
        return requests.get(News._base_url, params=self.payload).json()

    @staticmethod
    def _get_available_sorts():
        ret_val = {}
        if News._check_timestamp():
            LOGGER.info('Refreshing NewsAPI sources.')
            response = requests.get('https://newsapi.org/v1/sources').json()
            if response['status'] == 'ok':
                ret_val = {src['id']: src['sortBysAvailable'] for src in response['sources']}
            else:
                LOGGER.error("Server error. Coudn't get available sorts.")
            with open('data/avail_sort.yml', mode='w') as yml:
                yaml.dump({'timestamp': '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())},
                          yml,
                          default_flow_style=False)
                yaml.dump(ret_val, yml, default_flow_style=False)
        else:
            LOGGER.info('Loading sources from yaml file.')
            with open('data/avail_sort.yml') as yml:
                tmp = yaml.load(yml)
                tmp.pop('timestamp')
                ret_val = {val: tmp[val] for val in tmp}
        return ret_val

    @staticmethod
    def _check_timestamp():
        with open('data/avail_sort.yml') as as_yml:
            timestamp = datetime.datetime.strptime(yaml.load(as_yml)['timestamp'],
                                                   '%Y-%m-%d %H:%M:%S')
        if ((datetime.datetime.now() - timestamp).days) > 1:
            return True
        else:
            return False

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
