# Generated by Django 5.0.2 on 2024-03-02 14:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_remove_shipmentitem_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipmentitem',
            name='shipment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.shipment'),
        ),
        migrations.AlterField(
            model_name='shipmentitem',
            name='warehousestock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.warehousestock'),
        ),
        migrations.CreateModel(
            name='GatePass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gate_pass_number', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('container_number', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('shipment', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.shipment')),
            ],
        ),
    ]
