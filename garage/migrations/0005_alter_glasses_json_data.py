# Generated by Django 4.0.4 on 2022-05-17 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garage', '0004_alter_glasses_json_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='glasses',
            name='json_data',
            field=models.JSONField(blank=True, default=dict, verbose_name='JSON data'),
        ),
    ]
