# Generated by Django 3.1.5 on 2021-05-31 22:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('likedislike', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='likedislike',
            old_name='isdislike',
            new_name='isdisliked',
        ),
    ]
