# Generated by Django 5.0.7 on 2024-08-26 07:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clinic', '0016_remove_testtype_test_category_testcategory_tests'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testcategory',
            name='tests',
        ),
        migrations.AddField(
            model_name='testtype',
            name='test_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Clinic.testcategory'),
        ),
    ]
