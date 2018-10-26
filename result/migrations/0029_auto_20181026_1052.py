# Generated by Django 2.1.2 on 2018-10-26 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0028_auto_20181023_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ctngsample',
            name='result_ct',
            field=models.CharField(blank=True, default='ÂM TÍNH', max_length=50),
        ),
        migrations.AlterField(
            model_name='ctngsample',
            name='result_ng',
            field=models.CharField(blank=True, default='ÂM TÍNH', max_length=50),
        ),
        migrations.AlterField(
            model_name='ctngsample',
            name='sample_type',
            field=models.CharField(blank=True, default='Phết cổ tử cung', max_length=100),
        ),
        migrations.AlterField(
            model_name='hbvstandardcurve',
            name='name',
            field=models.CharField(default='2018-10-26', max_length=100),
        ),
        migrations.AlterField(
            model_name='hcvstandardcurve',
            name='name',
            field=models.CharField(default='2018-10-26', max_length=100),
        ),
        migrations.AlterField(
            model_name='hpvsample',
            name='sample_type',
            field=models.CharField(blank=True, default='Phết cổ tử cung', max_length=100),
        ),
    ]