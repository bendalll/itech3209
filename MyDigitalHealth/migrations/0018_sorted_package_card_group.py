# Generated by Django 2.0.5 on 2018-09-16 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MyDigitalHealth', '0017_auto_20180916_2301'),
    ]

    operations = [
        migrations.AddField(
            model_name='sorted_package',
            name='card_group',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='MyDigitalHealth.Card_Groups'),
        ),
    ]
