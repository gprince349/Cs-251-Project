# Generated by Django 2.2.6 on 2019-11-23 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travello', '0006_user_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='user_image',
        ),
        migrations.AddField(
            model_name='group_member',
            name='net',
            field=models.IntegerField(default=0),
        ),
    ]
