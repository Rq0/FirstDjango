# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-30 13:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribers',
            name='name',
            field=models.CharField(max_length=254),
        ),
    ]
