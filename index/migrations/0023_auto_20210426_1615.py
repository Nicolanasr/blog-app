# Generated by Django 3.1.8 on 2021-04-26 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0022_delete_lastupdated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]