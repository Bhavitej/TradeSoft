# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-07-28 16:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='company_logo',
            field=models.FileField(null=True, upload_to=b''),
        ),
    ]
