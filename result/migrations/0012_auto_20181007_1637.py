# Generated by Django 2.1 on 2018-10-07 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0011_auto_20181007_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hbvsample',
            name='lab_id',
            field=models.CharField(max_length=50, unique_for_month='added'),
        ),
    ]
