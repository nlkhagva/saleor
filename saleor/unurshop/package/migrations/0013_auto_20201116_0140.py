# Generated by Django 3.1 on 2020-11-15 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0012_gaduurpackage_received_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gaduurpackage',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gaduurpackage',
            name='received_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gaduurpackage',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]