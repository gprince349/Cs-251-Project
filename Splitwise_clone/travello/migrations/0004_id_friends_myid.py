# Generated by Django 2.2.6 on 2019-11-06 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travello', '0003_auto_20191106_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='id_friends',
            name='myid',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
