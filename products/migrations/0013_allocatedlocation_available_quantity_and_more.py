# Generated by Django 5.0.2 on 2024-03-02 09:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_alter_warehousestock_accepted_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='allocatedlocation',
            name='available_quantity',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='allocatedlocation',
            name='max_quantity',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
