# Generated by Django 3.1.12 on 2021-07-23 11:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ad', '0005_auto_20210722_2359'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='liked',
            field=models.ManyToManyField(blank=True, related_name='favourite_ads', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ad',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posted_ads', to=settings.AUTH_USER_MODEL),
        ),
    ]
