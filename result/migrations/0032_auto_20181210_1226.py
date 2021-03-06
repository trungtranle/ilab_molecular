# Generated by Django 2.1 on 2018-12-10 12:26

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0031_auto_20181110_0819'),
    ]

    operations = [
        migrations.CreateModel(
            name='HCVGenoSample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genotype', models.CharField(max_length=100)),
                ('curves', django.contrib.postgres.fields.jsonb.JSONField()),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='result.HCVSample')),
            ],
        ),
        migrations.AlterField(
            model_name='hbvstandardcurve',
            name='name',
            field=models.CharField(default='2018-12-10', max_length=100),
        ),
        migrations.AlterField(
            model_name='hcvstandardcurve',
            name='name',
            field=models.CharField(default='2018-12-10', max_length=100),
        ),
    ]
