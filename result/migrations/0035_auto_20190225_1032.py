# Generated by Django 2.1 on 2019-02-25 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0034_auto_20190225_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hcvgenosample',
            name='sample',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='result.HCVSample'),
        ),
    ]