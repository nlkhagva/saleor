# Generated by Django 3.1 on 2020-10-12 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0128_merge_20201008_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='available_for_purchase',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
