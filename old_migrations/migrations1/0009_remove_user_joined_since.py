# Generated by Django 5.0.6 on 2024-07-04 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article_hive_app', '0008_user_joined_since_alter_comment_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='joined_since',
        ),
    ]
