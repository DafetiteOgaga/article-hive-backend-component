# Generated by Django 5.0.6 on 2024-07-05 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_hive_app', '0014_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
    ]
