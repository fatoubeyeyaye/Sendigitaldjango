# Generated by Django 5.0.6 on 2025-03-10 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kercui', '0004_remove_rendezvous_user_rendezvous_patient_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rendezvous',
            old_name='patient',
            new_name='user',
        ),
    ]
