# Generated by Django 3.0.4 on 2020-04-08 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventCalendar', '0004_comment_post'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
