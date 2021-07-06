"""
WSGI config for chart_shirt project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application



path = '/home/iyraseshop/iyraseshop/chart_shirt'
if path not in sys.path:
    sys.path.insert(0, path)


os.environ['DJANGO_SETTINGS_MODULE'] = 'chart_shirt.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chart_shirt.settings')


application = get_wsgi_application()
