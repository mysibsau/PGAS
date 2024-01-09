from django.db import models

from .models import Document


class ModelMixin(models.Model):
    documents = models.ManyToManyField(Document, blank=True)

    class Meta:
        abstract = True
