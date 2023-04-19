# Generated by Django 4.2 on 2023-04-19 09:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("companies", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="submitted_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="added_companies",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
