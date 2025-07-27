from django.core.wsgi import get_wsgi_application
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Response

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chali_event_management.settings')
application = get_wsgi_application()

def handler(environ, start_response):
    return application(environ, start_response)
