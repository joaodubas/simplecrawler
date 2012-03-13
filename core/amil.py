#!/usr/bin/env python
# encoding: utf-8

"""Simple crawler to retrieve physicians registered on AMIL website.

By default retrieve cardiologists from AMIL 140 NACIONAL network from every
first city of all states and record on log.txt.

"""

import bs4
import urllib
import urllib2
from uf import Location

def _extract_names(root):
    """Extract the name of the physicians, contained on the html source.

    root -- a beautiful soup node.

    """
    results = root.find_all('div', 'resultado-tabela', limit=1)

    if not results:
        return ['Nenhum']

    names = []
    for result in results:
        rows = result.find_all('tr', 'titulo')
        for row in rows:
            name = row.find_all('th')[0].string
            names.append(name)

    return names


class Physician(object):
    """Obtain the physicans registered on AMIL portal."""
    base_url = 'http://www.amil.com.br/portal/servicos/rede-credenciada/buscar'

    def __init__(self, network='AMIL 140 NACIONAL', states=None):
        """Initialize the class, passing the choosen network.

        network -- a valid AMIL network.
        states -- a dictionary containing states as keys and list of cities as
                values, if not set, will use Location to retrieve the needed
                information.

        >>> p.get_physicians()
        >>> hasattr(p, 'physicians')
        True
        >>> 'PA:ABAETETUBA' in dict(p.physicians).keys()
        True

        """
        if not states:
            location = Location(network)
            states = location.states

        self.location = states
        self.physicians = []
        self.query = [
            ('filter.bairro', 'TODOS OS BAIRROS'),
            ('filter.contexto', 'AMIL'),
            ('filter.especialidade', 'CARDIOLOGIA'),
            ('filter.modalidade', 'saude'),
            ('filter.operadora', 'AMIL'),
            ('filter.redeCredenciada', network)
        ]

    def logger(self):
        """Write a log containing the [states:cities] [doctor name]."""
        log = open('medicos.txt', 'w')
        tmpl = '[%s] [%s]\n'

        self.get_physicians()
        for key, values in self.physicians:
            for physician in values:
                log.write(tmpl % (key, physician))

        log.close()

    def get_physicians(self):
        """Obtain the physicans from all states and cities."""
        states = self.location.keys()
        states.sort()
        for k in states:
            cities = self.location[k]
            self.get_physican(k, cities[0])

    def get_physican(self, state, city):
        """Obtain the physicians of a give state and city.

        state -- a two digit abbreviation for a state
        city -- a valid city name

        """
        query = self.query[:]
        query.append(('filter.municipio', city))
        query.append(('filter.estado', state))

        req = urllib2.urlopen(self.base_url, urllib.urlencode(query))
        source = req.read()
        root = bs4.BeautifulSoup(source)

        physicians = _extract_names(root)
        self.physicians.append(('%s:%s' % (str(state), str(city)), physicians))


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and '--test' in sys.argv:
        import doctest
        doctest.testmod(extraglobs={
            'p': Physician(),
        })
    else:
        cardiol = Physician()
        cardiol.logger()
