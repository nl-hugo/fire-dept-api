# Generated by Django 2.0.7 on 2018-08-02 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alarmeringen', '0002_auto_20180802_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alarmering',
            name='melding',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='alarmering',
            name='tekstmelding',
            field=models.CharField(max_length=500),
        ),
    ]