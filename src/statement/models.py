import os
import uuid
from collections import defaultdict
from datetime import datetime

from django.apps import apps
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModelMixin


class CustomQuerySet(models.QuerySet):
    def current_year(self):
        queryset = self.filter(create_at__year=datetime.now().year)
        if datetime.now().month >= 9:
            return queryset.filter(create_at__month__gte=9)
        return queryset


class CustomManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().prefetch_related('user', 'olympiads', 'olympiads__documents', 'olympiads__comments')
        )


class Statement(LifecycleModelMixin, models.Model):
    class Status(models.IntegerChoices):
        PENDING = 0, 'В обработке'
        APPROVED = 1, 'Одобрено'
        REJECTED = 2, 'Отклонено'

    id = models.UUIDField(_('ID'), default=uuid.uuid4, primary_key=True, editable=False, unique=True, db_index=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)

    objects = CustomManager.from_queryset(CustomQuerySet)()

    @cached_property
    def score(self) -> int:
        score = 0
        all_ahivments = self.achievements().values()
        for achievement in all_ahivments:
            for ahivment in achievement.filter(status=Statement.Status.APPROVED):
                score += ahivment.score
        return score

    @cached_property
    def preliminary_scores(self) -> int:
        score = 0
        all_ahivments = self.achievements().values()
        for achievement in all_ahivments:
            for ahivment in achievement:
                score += ahivment.preliminary_scores
        return score

    @cached_property
    def active(self) -> bool:
        this_year = datetime.now().year == self.create_at.year
        if datetime.now().month >= 9:
            return this_year and self.create_at.month >= 9
        return this_year

    @cached_property
    def term(self) -> int:
        if self.create_at.month >= 9:
            return 1
        return 2

    def achievements(self) -> dict[tuple[str, str], list]:
        models = apps.get_app_config('achievement').get_models()
        result = defaultdict(list)
        for model in models:
            plural = model._meta.verbose_name_plural
            model_name = model._meta.model_name
            result[(plural, model_name)] = model.objects.filter(statement=self)
        return dict(result)

    def pretty_status(self) -> str:
        html = '<span data-toggle="tooltip" data-placement="top" title="%s">%s</span>'
        status = {
            Statement.Status.PENDING: html % ('В обработке', '🤔'),
            Statement.Status.APPROVED: html % ('Принято', '✅'),
            Statement.Status.REJECTED: html % ('Отклонено', '❌'),
        }

        return status[self.status]

    @cached_property
    def card_background(self) -> str:
        number = int(self.id.hex, 16)

        backgrounds = []
        for _root, _dirs, files in os.walk('./statement/static/statement/backgrounds'):
            for file in files:
                if file.split('.')[-1] in ['jpg', 'jpeg', 'png']:
                    backgrounds.append(file)

        index = number % len(backgrounds)
        return f'statement/backgrounds/{backgrounds[index]}'
