# Generated by Django 2.0.7 on 2018-08-08 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alarmeringen', '0012_auto_20180808_1059'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alarmering',
            old_name='regio_link',
            new_name='regio',
        ),
    ]