# Generated by Django 3.0.6 on 2020-08-03 06:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0118_product_ushop'),
        ('unurshop', '0002_auto_20200627_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='shipping_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shipping_product', to='product.Product'),
        ),
    ]