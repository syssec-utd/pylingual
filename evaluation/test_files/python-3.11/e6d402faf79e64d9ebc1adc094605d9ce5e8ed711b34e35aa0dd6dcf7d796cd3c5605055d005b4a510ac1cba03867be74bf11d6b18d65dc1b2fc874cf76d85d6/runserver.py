from django.conf import settings
from django.contrib.staticfiles.management.commands.runserver import Command as DefaultRunserver
from importlib.util import find_spec
has_channels = find_spec('channels') is not None
if has_channels:
    from channels.management.commands.runserver import Command as ASGIRunserver
if has_channels and settings.SITE.use_linod:

    class Command(ASGIRunserver):
        pass
else:

    class Command(DefaultRunserver):
        pass