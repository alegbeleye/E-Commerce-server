# Generated by Django 4.2.4 on 2023-08-09 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0002_alter_customer_hashed_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='hashed_password',
            field=models.CharField(max_length=5000),
        ),
    ]
