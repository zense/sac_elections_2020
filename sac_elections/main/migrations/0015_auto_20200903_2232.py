# Generated by Django 3.1.1 on 2020-09-03 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_remove_userprofile_hasvoted'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together={('voter', 'category'), ('voter', 'candidate')},
        ),
    ]