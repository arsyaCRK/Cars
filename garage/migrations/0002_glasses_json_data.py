# Generated by Django 4.0.4 on 2022-05-16 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='glasses',
            name='json_data',
            field=models.JSONField(null=True, verbose_name='JSON data'),
        ),
    ]