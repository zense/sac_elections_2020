# Generated by Django 3.1.1 on 2020-09-03 05:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_userprofile_isadmin'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='category',
            field=models.CharField(default='NOBATCH', max_length=20),
        ),
        migrations.AlterField(
            model_name='vote',
            name='voter',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.RESTRICT, related_name='voter', to='main.userprofile'),
        ),
    ]
