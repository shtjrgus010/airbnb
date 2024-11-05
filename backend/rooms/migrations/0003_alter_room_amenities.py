# Generated by Django 5.1.2 on 2024-11-05 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rooms", "0002_room_category_alter_room_amenities_alter_room_owner"),
    ]

    operations = [
        migrations.AlterField(
            model_name="room",
            name="amenities",
            field=models.ManyToManyField(related_name="rooms", to="rooms.amenity"),
        ),
    ]