# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-24 03:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='sale_count',
            field=models.IntegerField(default=0),
        ),
    ]
