# Generated by Django 4.2.7 on 2023-12-02 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_nucleo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nucleo',
            old_name='projetcs',
            new_name='projects',
        ),
    ]
