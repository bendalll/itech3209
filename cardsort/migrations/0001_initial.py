# Generated by Django 2.1 on 2018-09-10 03:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_text', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Cards',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_name', models.CharField(max_length=200)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Packages',
            },
        ),
        migrations.CreateModel(
            name='UserCardsort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField(default='placeholder text')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cardsort.Package')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Saved Packages',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cardsort.Package'),
        ),
        migrations.AddField(
            model_name='card',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cardsort.Package'),
        ),
    ]
