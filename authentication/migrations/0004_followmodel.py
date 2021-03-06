# Generated by Django 3.2 on 2021-04-21 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_profile_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile')),
                ('following', models.ManyToManyField(blank=True, null=True, related_name='following_list', to='authentication.Profile')),
            ],
        ),
    ]
