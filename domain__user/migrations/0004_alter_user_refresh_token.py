# Generated by Django 5.2.1 on 2025-05-22 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domain__user', '0003_alter_user_access_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='refresh_token',
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name='refresh token'
            ),
        ),
    ]
