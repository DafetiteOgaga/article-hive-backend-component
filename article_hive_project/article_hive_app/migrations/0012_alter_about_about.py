# Generated by Django 5.0.7 on 2024-07-21 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_hive_app', '0011_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='about',
            name='about',
            field=models.TextField(max_length=10000),
        ),
    ]
