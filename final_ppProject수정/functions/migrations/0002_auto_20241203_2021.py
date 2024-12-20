# Generated by Django 3.1.12 on 2024-12-03 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='name_eng',
            new_name='name',
        ),
        migrations.AddField(
            model_name='game',
            name='capsule_image',
            field=models.URLField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='categories',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='game',
            name='coming_soon',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='game',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='genres',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='game',
            name='quarter',
            field=models.CharField(default=None, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='recommendations',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='game',
            name='release_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterModelTable(
            name='game',
            table='steam_game_game',
        ),
    ]
