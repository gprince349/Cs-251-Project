# Generated by Django 2.2.6 on 2019-11-23 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travello', '0004_id_friends_myid'),
    ]

    operations = [
        migrations.CreateModel(
            name='group_member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gid', models.IntegerField()),
                ('pid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='GROUP_MEMBERSHIP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.TextField()),
                ('gid', models.TextField()),
                ('group_name', models.TextField(max_length=100)),
                ('joined_date', models.TextField()),
                ('left_date', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='group_name',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
    ]
