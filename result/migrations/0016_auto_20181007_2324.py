# Generated by Django 2.1 on 2018-10-07 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0015_auto_20181007_2040'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Test',
        ),
        migrations.AlterField(
            model_name='hbvsample',
            name='lab_id',
            field=models.CharField(max_length=50, unique_for_year='added'),
        ),
        migrations.AlterField(
            model_name='hbvsample',
            name='sid',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
