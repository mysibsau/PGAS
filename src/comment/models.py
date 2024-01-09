import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Comment(models.Model):
    id = models.UUIDField(_("ID"), default=uuid.uuid4, primary_key=True, editable=False, unique=True, db_index=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    text = models.TextField()
    author = models.ForeignKey("user.User", on_delete=models.CASCADE)

    class Meta:
        ordering = ["create_at"]
