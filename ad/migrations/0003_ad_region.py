# Generated by Django 3.1.12 on 2021-07-22 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0002_auto_20210722_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='region',
            field=models.CharField(default='', max_length=100),
        ),
    ]
