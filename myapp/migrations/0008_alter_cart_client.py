# Generated by Django 3.2.5 on 2024-08-20 22:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_auto_20240820_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.client'),
        ),
    ]
