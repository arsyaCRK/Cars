# Generated by Django 4.0.4 on 2022-05-20 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garage', '0019_alter_glasses_json_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='glasses',
            name='json_data',
        ),
        migrations.AddField(
            model_name='vehicles',
            name='json_data',
            field=models.JSONField(null=True, verbose_name='JSON data'),
        ),
    ]
