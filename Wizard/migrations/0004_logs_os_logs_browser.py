# Generated by Django 5.1 on 2024-08-20 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Wizard', '0003_logs_delete_errors'),
    ]

    operations = [
        migrations.AddField(
            model_name='logs',
            name='OS',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='logs',
            name='browser',
            field=models.CharField(default=None, max_length=50),
        ),
    ]
