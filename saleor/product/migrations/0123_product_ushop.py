# Generated by Django 3.1 on 2020-08-28 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ushop', '0001_initial'),
        ('product', '0122_merge_20200818_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='ushop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ushop.shop'),
        ),
    ]
