# Generated by Django 5.0.2 on 2024-03-02 05:37

import datetime
import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_alter_transfernote_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='warehousestock',
            name='product_description',
        ),
        migrations.AddField(
            model_name='allocatedlocation',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 3, 2, 5, 37, 20, 401415, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='allocatedlocation',
            name='name',
            field=models.CharField(default=datetime.datetime(2024, 3, 2, 5, 37, 30, 501582, tzinfo=datetime.timezone.utc), max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='allocatedlocation',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='warehousestock',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='warehousestock',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='warehousestock',
            name='quantity',
            field=models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]