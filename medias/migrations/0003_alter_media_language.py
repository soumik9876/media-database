# Generated by Django 4.1.6 on 2023-03-15 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medias', '0002_alter_media_language_alter_media_region_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='language',
            field=models.CharField(blank=True, max_length=250, verbose_name='Language'),
        ),
    ]
