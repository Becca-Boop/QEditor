# Generated by Django 4.2.1 on 2023-12-02 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edit', '0016_metaattr_params_metaattr_return_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metaattr',
            name='params',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='metaattr',
            name='return_type',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]