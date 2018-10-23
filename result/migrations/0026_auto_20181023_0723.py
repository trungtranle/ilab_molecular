# Generated by Django 2.1 on 2018-10-23 07:23

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0025_auto_20181022_0901'),
    ]

    operations = [
        migrations.CreateModel(
            name='HPVSample',
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
                ('sample_type', models.CharField(blank=True, max_length=100)),
                ('test_kit', models.CharField(blank=True, max_length=50, null=True)),
                ('result_16_kt', models.CharField(blank=True, max_length=50, null=True)),
                ('result_18_kt', models.CharField(blank=True, max_length=50, null=True)),
                ('result_hr_kt', models.CharField(blank=True, max_length=50, null=True)),
                ('result_qual_va', models.CharField(blank=True, max_length=50, null=True)),
                ('result_type_va', models.CharField(blank=True, max_length=50, null=True)),
                ('img_va', models.ImageField(upload_to='img/')),
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
            field=models.CharField(default='2018-10-23', max_length=100),
        ),
        migrations.AlterField(
            model_name='hcvstandardcurve',
            name='name',
            field=models.CharField(default='2018-10-23', max_length=100),
        ),
    ]
