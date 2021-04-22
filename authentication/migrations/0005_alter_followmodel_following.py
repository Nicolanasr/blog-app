# Generated by Django 3.2 on 2021-04-21 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_followmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followmodel',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='following_list', to='authentication.Profile'),
        ),
    ]