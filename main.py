#!/usr/bin/env python
# encoding: utf-8

"""Execute core module and retrieves physicians registered on AMIL's website.

Physicians are recorded on ``medicos.txt`` file.

"""

if __name__ == '__main__':
    from core.amil import Physician

    cardiol = Physician()
    cardiol.logger()
