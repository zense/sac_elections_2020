# Generated by Django 3.1.1 on 2020-09-10 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_merge_20200910_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manifesto',
            name='agenda_1',
            field=models.TextField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='manifesto',
            name='agenda_2',
            field=models.TextField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='manifesto',
            name='agenda_3',
            field=models.TextField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='manifesto',
            name='intro',
            field=models.TextField(default='', max_length=600),
        ),
    ]
