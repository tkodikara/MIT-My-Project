# Generated by Django 5.0.2 on 2024-02-24 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_qty',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]