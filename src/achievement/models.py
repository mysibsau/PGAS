import uuid
from datetime import datetime

from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from comment.mixins import ModelMixin as CommentMixin
from document.mixins import ModelMixin as DocumentMixin
from statement.models import Statement


class Base(CommentMixin, DocumentMixin):
    id = models.UUIDField(_("ID"), default=uuid.uuid4, primary_key=True, editable=False, unique=True, db_index=True)
    name = models.CharField("Название", max_length=255)
    author = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="%(class)ss")
    statement = models.ForeignKey(Statement, on_delete=models.CASCADE, related_name="%(class)ss")
    status = models.IntegerField("Статус", choices=Statement.Status.choices, default=Statement.Status.PENDING)
    date = models.DateField("Дата проведения", default=datetime.now)

    class Meta:
        abstract = True

    def pretty_status(self) -> str:
        html = '<span data-toggle="tooltip" data-placement="top" title="%s">%s</span>'
        status = {
            Statement.Status.PENDING: html % ("В обработке", '🤔'),
            Statement.Status.APPROVED: html % ("Принято", '✅'),
            Statement.Status.REJECTED: html % ("Отклонено", '❌'),
        }

        return status[self.status]

    @cached_property
    def score(self) -> int:
        if self.status == Statement.Status.APPROVED:
            return self.preliminary_scores
        return 0

    @property
    def actual(self) -> bool:
        if datetime.now().month >= 9:
            return self.date.year == datetime.now().year
        return self.date.year == datetime.now().year - 1 or self.date.year == datetime.now().year


class Olympiad(Base):
    class Place(models.IntegerChoices):
        FIRST = 1, "🥇Первое"
        SECOND = 2, "🥈Второе"
        THIRD = 3, "🥉Третье"
        PARTICIPANT = 4, "Участник"

    class Level(models.IntegerChoices):
        INTERNATIONAL = 1, "Международный"
        FEDERAL = 2, "Всероссийский"
        DEPARTMENTAL = 3, "Ведомственный"
        INNER = 4, "Региональный"

    place = models.IntegerField("Занятое место", choices=Place.choices, default=Place.PARTICIPANT)
    level = models.IntegerField("Уровень олимпиады", choices=Level.choices, default=Level.INNER)

    @cached_property
    def preliminary_scores(self) -> int:
        table = {
            Olympiad.Level.INTERNATIONAL: [12, 11, 10, 8],
            Olympiad.Level.FEDERAL: [9, 8, 7, 5],
            Olympiad.Level.DEPARTMENTAL: [8, 7, 6, 4],
            Olympiad.Level.INNER: [7, 6, 5, 3],
        }
        return table[self.level][self.place - 1]

    class Meta:
        verbose_name = "Олимпиада"
        verbose_name_plural = "Олимпиады"


class Patent(Base):
    class Type(models.IntegerChoices):
        INVENTION = 1, "Патент на изобретение, свидетельство"
        UTILITY_MODEL = 2, "Патент на полезную модель"
        APPLICATION = 3, "Заявка"

    type = models.IntegerField("Тип патента", choices=Type.choices, default=Type.INVENTION)

    @cached_property
    def preliminary_scores(self) -> int:
        table = {
            Patent.Type.INVENTION: 30,
            Patent.Type.UTILITY_MODEL: 20,
            Patent.Type.APPLICATION: 5,
        }
        return table[self.type]

    class Meta:
        verbose_name = "Патент"
        verbose_name_plural = "Патенты"


class Article(Base):
    class Type(models.IntegerChoices):
        SCOPUS = 1, "Web of Science/Scopus"
        VAK = 2, "ВАК"
        RINC = 3, "РИНЦ"
        OTHER = 4, "Остальное"

    type = models.IntegerField("Тип публикации", choices=Type.choices, default=Type.OTHER)
    url = models.URLField('Ссылка')
    count_coauthors = models.IntegerField("Количество соавторов", default=0)

    @cached_property
    def preliminary_scores(self) -> int:
        table = {
            Article.Type.SCOPUS: 40,
            Article.Type.VAK: 30,
            Article.Type.RINC: 4,
            Article.Type.OTHER: 1,
        }
        return table[self.type]

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"
