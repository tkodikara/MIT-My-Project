# Generated by Django 5.0.2 on 2024-02-24 14:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_product_product_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qcstock',
            name='quantity',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
