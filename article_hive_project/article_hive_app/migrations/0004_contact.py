# Generated by Django 5.0.6 on 2024-07-04 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_hive_app', '0003_alter_comment_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=500)),
                ('user', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
