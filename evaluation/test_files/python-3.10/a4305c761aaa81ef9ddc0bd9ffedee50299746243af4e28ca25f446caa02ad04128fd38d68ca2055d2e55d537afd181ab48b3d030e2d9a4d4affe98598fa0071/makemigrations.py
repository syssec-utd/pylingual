from django.core.management.commands.makemigrations import Command as Parent
from ._migrations import monkeypatch_migrations
monkeypatch_migrations()

class Command(Parent):
    pass