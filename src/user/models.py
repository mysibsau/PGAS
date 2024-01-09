import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    id = models.UUIDField(_("ID"), default=uuid.uuid4, primary_key=True, editable=False, unique=True, db_index=True)
    group = models.CharField(max_length=10, blank=True, null=True)
    telegram_id = models.CharField(max_length=20, blank=True, null=True)
