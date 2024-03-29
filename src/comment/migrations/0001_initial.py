# Generated by Django 5.0.1 on 2024-01-09 02:49

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Comment',
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
                ('text', models.TextField()),
            ],
            options={
                'ordering': ['create_at'],
            },
        ),
    ]
