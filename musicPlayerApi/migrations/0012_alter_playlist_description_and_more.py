# Generated by Django 4.1.5 on 2023-02-10 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicPlayerApi', '0011_alter_playlist_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='Description',
            field=models.TextField(default='null'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='playlist',
            name='PlayListName',
            field=models.TextField(default='null'),
            preserve_default=False,
        ),
    ]
