# Generated by Django 2.0.7 on 2018-08-03 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alarmeringen', '0008_auto_20180803_1124'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alarmering',
            options={'ordering': ['-id'], 'verbose_name_plural': 'Alarmeringen'},
        ),
    ]