# Generated by Django 2.0.5 on 2018-09-10 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyDigitalHealth', '0005_auto_20180910_1144'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sorted_package',
            name='cards',
        ),
        migrations.AddField(
            model_name='sorted_package',
            name='card_group',
            field=models.ManyToManyField(to='MyDigitalHealth.Card_Groups'),
        ),
    ]
