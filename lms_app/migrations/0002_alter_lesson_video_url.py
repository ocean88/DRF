# Generated by Django 5.0.6 on 2024-05-15 17:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lms_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lesson",
            name="video_url",
            field=models.URLField(blank=True, null=True),
        ),
    ]
