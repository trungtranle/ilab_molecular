# Generated by Django 2.1 on 2018-10-07 09:28

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0009_auto_20181007_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hbvsample',
            name='curves',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
