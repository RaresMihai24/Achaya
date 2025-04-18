# Generated by Django 4.2.1 on 2025-04-19 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dragons', '0002_race_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='race',
            name='image',
        ),
        migrations.AddField(
            model_name='race',
            name='image_female',
            field=models.ImageField(blank=True, null=True, upload_to='races/female/'),
        ),
        migrations.AddField(
            model_name='race',
            name='image_male',
            field=models.ImageField(blank=True, null=True, upload_to='races/male/'),
        ),
    ]
