#!/usr/bin/env python
# encoding: utf-8

"""Helper module, that obtains states and cities available on AMIL website."""

import urllib
from crawler import Crawler
try:
    import json
except ImportError:
    import simplejson as json


class Location(object):
    """Obtain the state and city used by Amil."""
    base_url = 'http://www.amil.com.br/portal/servicos/rede-credenciada/%s'

    def __init__(self, network='AMIL 140 NACIONAL'):
        """Initialize the location, setting up a state property and the
        network that will be used to retrieve states and cities.

        network -- a valid AMIL network.

        >>> network = 'AMIL 140 NACIONAL'
        >>> hasattr(l, 'states')
        True
        >>> hasattr(l, 'query')
        True
        >>> dict(l.query)['filter.redeCredenciada'] == network
        True
        >>> 'SP' in l.states.keys()
        True
        >>> 'SAO PAULO' in l.states['SP']
        True

        """
        self.states = {}
        self.query = [
            ('filter.contexto', 'AMIL'),
            ('filter.modalidade', 'saude'),
            ('filter.operadora', 'AMIL'),
            ('filter.redeCredenciada', network)
        ]
        self.crawler = Crawler()
        self.initialize()

    def initialize(self):
        """Initialize the class obtaining states and cities, and closes the
        crawler at the end.

        """
        self.get_state()
        self.get_cities()
        self.crawler.close_browser()

    def _prepare_url(self, add_url, *args):
        """Prepare a url, adding to it the end of pathname and the proper
        querystring.

        """
        query = self.query[:]
        if args:
            query.extend(args)

        url = self.base_url % (add_url % (urllib.urlencode(query)), )
        return url

    def get_state(self):
        """Retrieve all states from the AMIL database, based on the selected
        network.

        """
        state_url = self._prepare_url('estados.json?%s')
        self.crawler.navigate_to(state_url)

        source = self.crawler.page_source()
        source = source[source.find('{'):source.find('}') + 1]
        source_json = json.loads(source)

        for k in source_json['estados']:
            self.states.setdefault(k, [])

    def get_cities(self):
        """Retrieves all cities, based on the states available."""
        for k in self.states.iterkeys():
            self.get_city(k)

    def get_city(self, state):
        """Retrieve a city, based on the selected state.

        state -- a two digit abbreviation for a state

        """
        city_url = self._prepare_url('municipios.json?%s',
            ('filter.estado', state))
        self.crawler.navigate_to(city_url)

        source = self.crawler.page_source()
        source = source[source.find('{'):source.find('}') + 1]
        source_json = json.loads(source)

        self.states[state].extend(source_json.get('municipios', []))


if __name__ == '__main__':
    import doctest
    doctest.testmod(extraglobs={
        'l': Location(),
    })
