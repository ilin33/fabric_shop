# Generated by Django 5.2 on 2025-05-08 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siteinfo',
            name='email',
        ),
        migrations.AddField(
            model_name='siteinfo',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='site_images/', verbose_name='Зображення'),
        ),
    ]
