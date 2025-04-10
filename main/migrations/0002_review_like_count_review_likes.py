# Generated by Django 4.2 on 2023-04-23 12:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="like_count",
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="review",
            name="likes",
            field=models.ManyToManyField(
                blank=True,
                default=None,
                related_name="likes",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
