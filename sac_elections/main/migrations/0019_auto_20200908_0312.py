# Generated by Django 3.1.1 on 2020-09-07 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20200907_0138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='salt',
            field=models.CharField(default='nosalt', max_length=30),
        ),
    ]