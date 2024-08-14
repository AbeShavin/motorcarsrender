# Generated by Django 5.0.6 on 2024-08-07 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("car_listing", "0023_remove_car_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="car",
            name="latitude",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="car",
            name="longitude",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="car",
            name="mileage",
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name="car",
            name="year",
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name="car",
            name="zipcode",
            field=models.PositiveIntegerField(),
        ),
    ]