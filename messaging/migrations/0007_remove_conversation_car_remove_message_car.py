# Generated by Django 5.0.6 on 2024-07-30 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("messaging", "0006_conversation_car"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="conversation",
            name="car",
        ),
        migrations.RemoveField(
            model_name="message",
            name="car",
        ),
    ]