"""Initial for settings app."""
import os

configuration = os.environ.get('DJANGO_ENV', 'dev')

from .common import *

if configuration == 'dev':
    from .dev import *
