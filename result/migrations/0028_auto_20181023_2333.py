# Generated by Django 2.1 on 2018-10-23 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0027_auto_20181023_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hpvsample',
            name='result_16_kt',
            field=models.CharField(blank=True, default='ÂM TÍNH', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='hpvsample',
            name='result_18_kt',
            field=models.CharField(blank=True, default='ÂM TÍNH', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='hpvsample',
            name='result_hr_kt',
            field=models.CharField(blank=True, default='ÂM TÍNH', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='hpvsample',
            name='result_qual_va',
            field=models.CharField(blank=True, default='ÂM TÍNH', max_length=50, null=True),
        ),
    ]