# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-30 09:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginApp', '0004_userprofile_idno'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('views', models.IntegerField(default=0)),
            ],
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='photo',
            field=models.ImageField(blank=True, upload_to='profile_photo'),
        ),
    ]
