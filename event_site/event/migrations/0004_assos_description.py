# Generated by Django 2.2.1 on 2019-06-06 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_auto_20190524_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='assos',
            name='description',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
