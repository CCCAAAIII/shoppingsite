# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-22 07:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='header',
            field=models.ImageField(default='customer/img/face1.jpg', null=True, upload_to='customer\\header'),
        ),
    ]