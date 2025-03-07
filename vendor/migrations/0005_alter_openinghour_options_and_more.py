# Generated by Django 5.1.6 on 2025-03-07 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0004_openinghour'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='openinghour',
            options={'ordering': ('day', 'from_hour')},
        ),
        migrations.AlterUniqueTogether(
            name='openinghour',
            unique_together={('day', 'from_hour', 'to_hour')},
        ),
    ]
