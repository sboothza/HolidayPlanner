# Generated by Django 5.1.1 on 2024-09-12 13:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("HolidayPlanner", "0002_weather"),
    ]

    operations = [
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "managed": False,
            },
        ),
    ]
