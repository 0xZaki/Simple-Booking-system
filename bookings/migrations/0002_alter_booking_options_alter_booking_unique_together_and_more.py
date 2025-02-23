# Generated by Django 5.1.6 on 2025-02-23 23:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="booking",
            options={"verbose_name_plural": "Bookings"},
        ),
        migrations.AlterUniqueTogether(
            name="booking",
            unique_together=set(),
        ),
        migrations.AddIndex(
            model_name="booking",
            index=models.Index(fields=["user"], name="bookings_bo_user_id_0e7f91_idx"),
        ),
    ]
