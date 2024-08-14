# Generated by Django 5.0.6 on 2024-08-09 17:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("car_listing", "0025_alter_car_make_alter_car_model"),
    ]

    operations = [
        migrations.AlterField(
            model_name="car",
            name="make",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="car_listing.carmake"
            ),
        ),
        migrations.AlterField(
            model_name="car",
            name="model",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="car_listing.carmodel"
            ),
        ),
        migrations.AlterField(
            model_name="carmodel",
            name="make",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="car_listing.carmake"
            ),
        ),
    ]