# Generated by Django 5.0.1 on 2024-01-09 02:49

import uuid

import django_lifecycle.mixins
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Statement',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name='ID',
                    ),
                ),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                (
                    'status',
                    models.IntegerField(
                        choices=[(0, 'В обработке'), (1, 'Одобрено'), (2, 'Отклонено')],
                        default=0,
                    ),
                ),
            ],
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
    ]
