# Generated by Django 4.2.4 on 2023-08-12 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0005_product_current_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='hashed_password',
            field=models.CharField(max_length=5000),
        ),
    ]
