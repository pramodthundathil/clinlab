# Generated by Django 5.0.7 on 2024-07-26 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0003_alter_patient_address_alter_patient_date_of_birth_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='date_of_birth',
        ),
        migrations.AddField(
            model_name='patient',
            name='age',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
