# Generated by Django 5.0.3 on 2024-04-09 15:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edit', '0020_remove_metaattr_order_remove_metapage_order_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemToItemLinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('success', models.BooleanField(default=False)),
                ('response', models.TextField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='SecondaryKey', to='edit.qobject')),
                ('npc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='PrimaryKey', to='edit.qobject')),
            ],
        ),
    ]