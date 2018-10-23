# Generated by Django 2.1 on 2018-10-19 02:11

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0022_hbvsample_std_curve'),
    ]

    operations = [
        migrations.CreateModel(
            name='HCVSample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateField(default=django.utils.timezone.now)),
                ('lab_id', models.CharField(max_length=50, unique_for_year='added')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('sid', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('age', models.CharField(blank=True, max_length=4, null=True)),
                ('sex', models.CharField(blank=True, max_length=10)),
                ('address', models.CharField(blank=True, max_length=200)),
                ('doctor', models.CharField(blank=True, max_length=100)),
                ('clinic', models.CharField(blank=True, max_length=100, null=True, verbose_name='Đơn vị gửi mẫu')),
                ('dx', models.CharField(blank=True, max_length=400)),
                ('result', models.CharField(blank=True, max_length=50)),
                ('ct', models.FloatField(blank=True, null=True)),
                ('copies', models.FloatField(blank=True, null=True)),
                ('finished', models.BooleanField(default=False)),
                ('curves', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
            options={
                'ordering': ('-added',),
            },
        ),
        migrations.AlterField(
            model_name='hbvstandardcurve',
            name='name',
            field=models.CharField(default='2018-10-19', max_length=100),
        ),
        migrations.AlterField(
            model_name='hcvstandardcurve',
            name='name',
            field=models.CharField(default='2018-10-19', max_length=100),
        ),
    ]