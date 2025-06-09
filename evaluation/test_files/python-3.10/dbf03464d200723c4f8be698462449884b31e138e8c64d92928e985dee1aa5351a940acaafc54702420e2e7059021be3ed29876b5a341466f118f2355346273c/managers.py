from django.db import models

class ValidSignatureCaptureManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(document__in_trash=False)