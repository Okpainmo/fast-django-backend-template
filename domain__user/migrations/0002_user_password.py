# Generated by Django 5.2.1 on 2025-05-22 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domain__user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='password'),
        ),
    ]
