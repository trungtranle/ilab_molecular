# Generated by Django 2.1 on 2019-02-25 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('result', '0035_auto_20190225_1032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hcvgenosample',
            name='id',
        ),
        migrations.AlterField(
            model_name='hcvgenosample',
            name='sample',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='result.HCVSample'),
        ),
    ]
