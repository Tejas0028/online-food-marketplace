# Generated by Django 5.1.6 on 2025-03-07 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0005_alter_openinghour_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='openinghour',
            options={'ordering': ('day', '-from_hour')},
        ),
        migrations.AlterUniqueTogether(
            name='openinghour',
            unique_together={('vendor', 'day', 'from_hour', 'to_hour')},
        ),
    ]
