# Generated by Django 2.1 on 2018-10-16 06:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0021_auto_20181016_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='hbvsample',
            name='std_curve',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='result.HBVStandardCurve'),
        ),
    ]
