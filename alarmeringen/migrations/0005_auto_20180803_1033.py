# Generated by Django 2.0.7 on 2018-08-03 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alarmeringen', '0004_auto_20180802_1234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alarmering',
            name='subitems',
        ),
        migrations.AddField(
            model_name='alarmering',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subitems', to='alarmeringen.Alarmering'),
        ),
    ]
