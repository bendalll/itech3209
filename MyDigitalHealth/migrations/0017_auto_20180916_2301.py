# Generated by Django 2.0.5 on 2018-09-16 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyDigitalHealth', '0016_auto_20180916_2223'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sorted_package',
            name='cards',
        ),
        migrations.AddField(
            model_name='sorted_package',
            name='cards',
            field=models.ManyToManyField(to='MyDigitalHealth.Cards'),
        ),
    ]
