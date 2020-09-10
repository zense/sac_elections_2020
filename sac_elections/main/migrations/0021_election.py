# Generated by Django 3.1.1 on 2020-09-09 16:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_manifesto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startTime', models.DateTimeField(default=datetime.datetime(2020, 9, 6, 22, 11, 49, 664017), verbose_name='voted on')),
                ('endTime', models.DateTimeField(default=datetime.datetime(2021, 7, 6, 22, 11, 49, 664042), verbose_name='voted on')),
            ],
        ),
    ]