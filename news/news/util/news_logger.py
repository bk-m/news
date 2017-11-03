# -*- coding: utf-8 -*-

"""
Logger set up for News package.
"""

import logging

ROOT = logging.getLogger()
FORMAT = '%(asctime)-19s %(levelname)-8s %(module)-11s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')

# disable requests' debug logging
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
