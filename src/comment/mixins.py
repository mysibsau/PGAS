from django.db import models
from django.utils.functional import cached_property

from .models import Comment


class ModelMixin(models.Model):
    comments = models.ManyToManyField(Comment, blank=True)

    class Meta:
        abstract = True

    @cached_property
    def comment_text(self) -> str:
        count = self.comments.count()
        if count == 0:
            return "Комментариев нет"
        elif count == 1:
            return "1 комментарий"
        elif count < 5:
            return f"{count} комментария"
        return f"{count} комментариев"
