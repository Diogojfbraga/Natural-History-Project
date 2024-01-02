# Generated by Django 4.2.3 on 2023-12-31 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('specimen_catalog', '0003_remove_specimen_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='specimen',
            name='continent',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='specimen',
            name='country',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]