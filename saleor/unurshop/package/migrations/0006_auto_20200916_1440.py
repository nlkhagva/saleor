# Generated by Django 3.1 on 2020-09-16 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0096_auto_20200916_1437'),
        ('package', '0005_auto_20200914_1452'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='packageline',
            name='orderline',
        ),
        migrations.AddField(
            model_name='packageline',
            name='fulfilmentline',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='order.fulfillmentline'),
        ),
    ]
