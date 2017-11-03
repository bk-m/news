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

import requests


class IllegalArgumentError(ValueError):
    pass


class News():
    _base_url = 'https://newsapi.org/v1/articles'
    _api_key = '175b17969f3141fbb2af57b2b61e669e'

    def __init__(self, source=None, sort='latest'):
        if not source:
            raise IllegalArgumentError('Must pass a source')
        tmp = requests.get('https://newsapi.org/v1/sources').json()

        self.payload = {'source': source, 'sortBy': sort, 'apiKey': News._api_key}

    def get_news(self):
        response = requests.get(News._base_url, params=self.payload).json()
        if response['status'] == 'error' and response['code'] == 'sourceUnavailableSortedBy':
            del self.payload['sortBy']
            response = requests.get(News._base_url, params=self.payload)
        return response

def main():
    ids = ['hacker-news', 'spiegel-online']
    tmp = [News(val).get_news() for val in ids]

    for resp in tmp:
        print('Source: {}'.format(resp.json()['source']))
        for article in resp.json()['articles']:
            print(article['title'])
        print('-------------------------------------------------------------------------')

if __name__ == '__main__':
    main()
