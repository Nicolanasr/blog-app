# Generated by Django 3.1.8 on 2021-04-26 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0018_auto_20210426_1524'),
    ]

    operations = [
        migrations.CreateModel(
            name='mostRatedForTheWeek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.post')),
            ],
        ),
    ]