# Generated by Django 5.1.6 on 2025-03-10 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='tax_date',
            new_name='tax_data',
        ),
    ]
