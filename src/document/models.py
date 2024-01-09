import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Document(models.Model):
    id = models.UUIDField(_("ID"), default=uuid.uuid4, primary_key=True, editable=False, unique=True, db_index=True)
    file = models.FileField(upload_to="documents")
    author = models.ForeignKey("user.User", on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name.split("/")[-1]
