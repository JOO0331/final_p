# Generated by Django 3.1.12 on 2024-11-20 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('steam_game', '0002_auto_20241120_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamereview',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]