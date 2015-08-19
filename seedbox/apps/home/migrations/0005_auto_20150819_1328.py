# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20150819_1324'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectpage',
            old_name='image',
            new_name='previewimage',
        ),
    ]
