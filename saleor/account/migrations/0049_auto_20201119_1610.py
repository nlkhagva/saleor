# Generated by Django 3.1 on 2020-11-19 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0048_user_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]
