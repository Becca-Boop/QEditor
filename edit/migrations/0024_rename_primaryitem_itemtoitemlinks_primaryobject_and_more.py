# Generated by Django 5.0.3 on 2024-04-16 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('edit', '0023_rename_npc_itemtoitemlinks_primaryitem_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itemtoitemlinks',
            old_name='primaryitem',
            new_name='primaryobject',
        ),
        migrations.RenameField(
            model_name='itemtoitemlinks',
            old_name='secondaryitem',
            new_name='secondaryobject',
        ),
    ]
