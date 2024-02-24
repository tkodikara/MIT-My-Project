# Generated by Django 5.0.2 on 2024-02-24 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_remove_product_product_qty_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qcstock',
            old_name='date_accepted',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='qcstock',
            old_name='accepted_by',
            new_name='updated_by',
        ),
        migrations.AddField(
            model_name='qcstock',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]