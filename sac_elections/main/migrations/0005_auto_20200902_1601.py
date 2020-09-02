# Generated by Django 3.1.1 on 2020-09-02 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20200902_1322'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='batch',
            new_name='batch_programme',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='batch_year',
            field=models.CharField(default='0000', max_length=10),
        ),
        migrations.AddField(
            model_name='vote',
            name='voter',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.RESTRICT, related_name='voter', to='main.userprofile'),
        ),
    ]
