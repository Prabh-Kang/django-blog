# Generated by Django 3.0.8 on 2020-07-23 11:52

import blogapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0003_auto_20200723_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='image',
            field=models.ImageField(blank=True, default='default-prof-pic.jpg', null=True, upload_to=blogapp.models.upload_location),
        ),
    ]