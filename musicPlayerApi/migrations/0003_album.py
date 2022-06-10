# Generated by Django 4.0.3 on 2022-06-10 00:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('musicPlayerApi', '0002_remove_category_musicid_music_categoryid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CreatedAt', models.DateField(default=django.utils.timezone.now)),
                ('MusicId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musicPlayerApi.music')),
                ('UserId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Album',
            },
        ),
    ]