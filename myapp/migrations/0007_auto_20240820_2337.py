# Generated by Django 3.2.5 on 2024-08-20 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_cart_cartitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='user',
            new_name='client',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]
