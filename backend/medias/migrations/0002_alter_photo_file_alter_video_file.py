# Generated by Django 5.1.2 on 2024-11-19 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("medias", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="photo",
            name="file",
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name="video",
            name="file",
            field=models.URLField(),
        ),
    ]
