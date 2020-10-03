# Generated by Django 3.1 on 2020-08-31 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_video_video_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='keywords',
            new_name='keywordsGoogle',
        ),
        migrations.RemoveField(
            model_name='product',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='product',
            name='weight',
        ),
        migrations.AddField(
            model_name='product',
            name='keywordsSite',
            field=models.TextField(blank=True, null=True),
        ),
    ]