# Generated by Django 2.1 on 2018-10-15 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0017_auto_20181015_1403'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hbvsample',
            name='std_curve',
        ),
        migrations.AddField(
            model_name='hbvstandardcurve',
            name='B',
            field=models.FloatField(default=1.3),
            preserve_default=False,
        ),
    ]
