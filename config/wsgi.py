import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Lance les migrations automatiquement au démarrage
from django.core.management import call_command
try:
    call_command('migrate', '--run-syncdb', verbosity=0)
except Exception:
    pass

application = get_wsgi_application()
