# Generated by Django 3.1 on 2020-12-11 22:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0103_remove_fulfillmentline_package_line'),
        ('package', '0017_auto_20201201_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packageline',
            name='fulfillmentline',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.fulfillmentline'),
        ),
    ]