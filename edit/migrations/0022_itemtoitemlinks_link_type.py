# Generated by Django 5.0.3 on 2024-04-10 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edit', '0021_itemtoitemlinks'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemtoitemlinks',
            name='link_type',
            field=models.CharField(default=None, max_length=12),
        ),
    ]
