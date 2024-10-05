"""
ASGI config for smartSprout project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
# from django.core.asgi import get_asgi_application
import django
from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartSprout.settings')
django.setup()

application = get_default_application()
