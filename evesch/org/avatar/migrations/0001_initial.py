# Generated by Django 2.1.8 on 2019-04-22 22:50

import datetime
from django.db import migrations, models
import evesch.org.avatar.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary', models.BooleanField(default=False)),
                ('avatar', models.ImageField(blank=True, max_length=1024, upload_to=evesch.org.avatar.models.avatar_file_path)),
                ('date_uploaded', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
    ]