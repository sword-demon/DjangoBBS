# Generated by Django 2.2 on 2021-07-14 22:37

import bbs.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0006_auto_20210714_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='avatar',
            field=models.FileField(default='/avatars/avatar.jpg', upload_to=bbs.models.user_directory_path),
        ),
    ]
